import os
import argparse
import logging
import re
import math

import nltk
import googleapiclient.discovery
import googleapiclient.errors
from deepmultilingualpunctuation import PunctuationModel
from youtube_transcript_api import YouTubeTranscriptApi

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

logging.basicConfig(level=logging.INFO, force=True)

def clean_for_filename(title):
    # Define a regular expression to keep only alphanumeric characters, spaces, dots, hyphens, and various parentheses
    cleaned_title = re.sub(r'[^\w\s\.\-\(\)\[\]]', '', title)
    
    # Remove leading and trailing spaces
    return cleaned_title.strip()

def remove_music_tags(text):
    # Remove [Music] or [music]
    updated_text = re.sub(r'\[music\]', '', text, flags=re.IGNORECASE)
    return updated_text

def remove_period_after_hashes(text):
    # Remove . after # or ##, considering newline characters
    return re.sub(r'(#\.|##\.)', lambda match: match.group(1)[:-1], text)

def remove_escape_sequences(text):
    # Some old videos contain escape sequences like \n in their subtitle
    # Remove \n, \r\n, \t, \b, \r
    return re.sub(r'\\[nrtb]|\\r\n', '', text)

def remove_double_greater_than(text):
    # Replace occurrences of ">>" with an empty string
    cleaned_text = re.sub(r'>>', '', text)
    return cleaned_text

def add_punctuation(text, punctuation_model):
    if punctuation_model != "":
        model = PunctuationModel(model=punctuation_model)
    else:
        model = PunctuationModel()
        punctuated_text = model.restore_punctuation(text)
    return punctuated_text

def capitalize_sentences(sentences):
    # Capitalize the first letter of each sentence in a batch
    capitalized_sentences = [sentence[0].upper() + sentence[1:] for sentence in sentences]
    return capitalized_sentences

def parse_youtube_url(url):
    video_id_match = re.search(r'(?:youtube\.com\/.*?[?&]v=|youtu\.be\/)([^"&?\/\s]{11})', url)
    if video_id_match:
        return video_id_match.group(1)
    else:
        raise ValueError('Invalid YouTube URL')

def parse_chapters(description):
    lines = description.split("\n")
    regex = re.compile(r"(\d{0,2}:?\d{1,2}:\d{2})")
    chapters = []

    for line in lines:
        matches = regex.findall(line)
        if matches:
            ts = matches[0]
            title = line.replace(ts, "").strip()

            # Check if the title contains another timestamp and remove it
            title = re.sub(r'\d{0,2}:?\d{1,2}:\d{2}', '', title).strip().strip('-').strip().strip('-').strip()

            chapters.append({
                "timestamp": ts,
                "title": title,
            })

    return chapters

def get_transcript(video_id, language, video_info, verbose=True):
    transcript_list = youtube_transcript_api.YouTubeTranscriptApi.get_transcript(video_id, languages=[language])
    
    if video_info["title"] != "":
        transcript = f'# {video_info["title"]}\n\n'
    
    current_chapter_index = 0
    chapters = video_info["chapters"]
    logging.info(f"Transcript_List Length: {len(transcript_list)}, Chapter Length: {len(chapters)}")
    
    for i, line in enumerate(transcript_list):
        start_time = int(math.floor(line['start']))  # Floor and convert to integer

        # Check if current_chapter_index is within the valid range
        if 0 <= current_chapter_index < len(chapters):
            chapter_time = chapters[current_chapter_index]['timestamp']

            try:
                # Extract start time from the chapter timestamp
                chapter_start = chapter_time.strip()
                chapter_start_seconds = sum(int(x) * 60 ** i for i, x in enumerate(reversed(chapter_start.split(':'))))
                chapters[current_chapter_index]["title"] = chapters[current_chapter_index]["title"].strip()
                buffer_time = 2
                
                if start_time >= chapter_start_seconds - buffer_time:
                    logging.info(f'\n\n## {chapters[current_chapter_index]["title"]}\n')
                    current_chapter_index += 1
            except Exception as e:
                logging.error(f"Error processing chapter timestamp: {chapter_time}")
                logging.error(f"Error details: {e}")
        
        line['text'] = remove_music_tags(line['text'])
        line['text'] = remove_escape_sequences(line['text'])
        line['text'] = remove_double_greater_than(line['text'])
        if line['text']:
          transcript += line['text'].strip() + ' '
        
        # Log progress information
        if verbose and i % 100 == 0:  # Adjust the log frequency as needed
            logging.info(f"Processed {i} lines out of {len(transcript_list)}")

    return transcript

def process_and_save_transcript(video_id, video_info, language, generate_punctuated, output_dir, filename, verbose, punctuation_model):
    try:
        raw_transcript = get_transcript(video_id, language, video_info, verbose)
        logging.info("Raw Transcript Length: %d", len(raw_transcript))
        
        if generate_punctuated:
            with_punctuation = add_punctuation(raw_transcript, punctuation_model)
            with_punctuation = remove_period_after_hashes(with_punctuation)
            logging.info("Punctuation Char Length: %d", len(with_punctuation))
            sentences = nltk.sent_tokenize(with_punctuation)
            logging.info("Sentences to process, (punctuated): %d", len(sentences))
        else:
            sentences = nltk.sent_tokenize(raw_transcript)
            logging.info("Sentences to process, (raw): %d", len(sentences))

        # Capitalize sentences without batching
        capitalized_sentences = capitalize_sentences(sentences)
        
        double_linesep = os.linesep + os.linesep
        capitalized_transcript = double_linesep.join(capitalized_sentences)
        output_path = os.path.join(output_dir, f'{filename}.md')
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(capitalized_transcript)
            
        if generate_punctuated:
            logging.info(f'Punctuated transcript saved to {output_path}')
        else:
            logging.info(f'Raw transcript saved to {output_path}')

    except Exception as e:
        logging.error(f'Error: {e}')

def getVideoInfo (video_id):
  try:
    # Set up Google API credentials using API key
    api_key =  userdata.get('GOOGLE_API_KEY') # Replace with your actual API key
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
    request = youtube.videos().list(part="id,snippet",
                                id = video_id
        )
    response = request.execute()
    title = response['items'][0]['snippet']['title']
    description = response['items'][0]['snippet']['description']
    data = {"title" : title, "chapters" : parse_chapters(description)}
    return data
  except Exception as e:
    logging.error(f'Error: {e}')
    return {"title": "", "chapters": []}

def main():

    video_id = parse_youtube_url(args.url)
    video_info = getVideoInfo(video_id)

    language = args.language or "en"

    output_dir = args.output or os.getcwd()
    filename = video_info["title"] if video_info["title"] else video_id
    batch_size = args.batch_size or 0  # 0 will automatically determine batch size

    process_and_save_transcript(video_id, video_info, language, args.punctuated, output_dir, filename, batch_size,
                                args.verbose, args.punctuation_model)
    
def main():
    parser = argparse.ArgumentParser(description='Process YouTube video transcript and save it.')
    parser.add_argument('url', type=str, help='YouTube video URL')
    parser.add_argument('-l', '--language', type=str, default='en', help='Language for the transcript (default: en)')
    parser.add_argument('-p', '--punctuated', action='store_true', help='Generate punctuated transcript (default: False)')
    parser.add_argument('-o', '--output_dir', type=str, default='.', help='Output directory for saving the transcript (default: .)')
    parser.add_argument('-f', '--filename', type=str, default='', help='Filename for saving the transcript (default: Video Title or Video Id)')
    parser.add_argument('-m', '--punctuation_model', type=str, default='', help='Path to the punctuation model (default: None)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Print verbose output (default: False)')

    args = parser.parse_args()

    video_id = parse_youtube_url(args.url)
    video_info = getVideoInfo(video_id)
    filename = args.filename or clean_for_filename(video_info["title"]) or clean_for_filename(video_id)

    process_and_save_transcript(video_id, video_info, args.language, args.punctuated, args.output_dir, filename, args.verbose, args.punctuation_model)

if __name__ == "__main__":
    main()
