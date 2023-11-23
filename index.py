import os
import argparse
import youtube_transcript_api
from deepmultilingualpunctuation import PunctuationModel
from nltk import sent_tokenize
from multiprocessing import Pool
import time
import logging
import re
import math
import nltk
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

def remove_music_tags(text):
    # Remove [Music] or [music]
    updated_text = re.sub(r'\[music\]', '', text, flags=re.IGNORECASE)
    return updated_text

def get_transcript(video_id, language, video_info, verbose=True):
    transcript_list = youtube_transcript_api.YouTubeTranscriptApi.get_transcript(video_id, languages=[language])
    if video_info["title"] != "":
        transcript = f'# {video_info["title"]}\n\n'
    current_chapter_index = 0
    chapters = video_info["chapters"]

    for line in transcript_list:
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
                    transcript += f'\n\n## {chapters[current_chapter_index]["title"]}\n'
                    current_chapter_index += 1
            except Exception as e:
                print(f"Error processing chapter timestamp: {chapter_time}")
                print(f"Error details: {e}")
        line['text'] = remove_music_tags(line['text'])
        transcript += line['text'].strip() + ' '

    return transcript

def remove_period_after_hashes(text):
    # Remove . after ##, considering newline characters
    updated_text = re.sub(r'(?<=##)[.\n]+', '', text)
    return updated_text

def add_punctuation(text, punctuation_model):
    if punctuation_model != "":
        model = PunctuationModel(model=punctuation_model)
    else:
        model = PunctuationModel()
        punctuated_text = model.restore_punctuation(text)
    return punctuated_text

def capitalize_sentences_batch(sentences):
    # Capitalize the first letter of each sentence in a batch
    capitalized_sentences = [sentence[0].upper() + sentence[1:] for sentence in sentences]
    return capitalized_sentences

def process_and_save_transcript(video_id, video_info, language, generate_punctuated, output_dir, filename, batch_size, verbose, punctuation_model):
    try:
        raw_transcript = get_transcript(video_id, language, video_info, verbose)

        if generate_punctuated:
            with_punctuation = add_punctuation(raw_transcript, punctuation_model)
            with_punctuation = remove_period_after_hashes(with_punctuation)
            sentences = sent_tokenize(with_punctuation)
            num_processes = os.cpu_count() or 1
            batch_size = 2 ** int(math.log2(batch_size)) if batch_size else num_processes

            with Pool() as pool:
                capitalized_sentences = list(
                    pool.imap(capitalize_sentences_batch, [sentences[i:i + batch_size] for i in
                                                            range(0, len(sentences), batch_size)]))
            capitalized_transcript = os.linesep.join(
                [sentence for batch in capitalized_sentences for sentence in batch])
            output_path = os.path.join(output_dir, f'{filename}.md')
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(capitalized_transcript)
            logging.info(f'Punctuated transcript saved to {output_path}')
        else:
            sentences = sent_tokenize(raw_transcript)
            num_processes = os.cpu_count() or 1
            batch_size = 2 ** int(math.log2(batch_size)) if batch_size else num_processes

            with Pool() as pool:
                capitalized_sentences = list(
                    pool.imap(capitalize_sentences_batch, [sentences[i:i + batch_size] for i in
                                                            range(0, len(sentences), batch_size)]))
            capitalized_transcript = os.linesep.join(
                [sentence for batch in capitalized_sentences for sentence in batch])
            output_path = os.path.join(output_dir, f'{filename}.md')
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(capitalized_transcript)
            logging.info(f'Raw transcript saved to {output_path}')

    except Exception as e:
        logging.error(f'Error: {e}')


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

def getVideoInfo(video_id):
    try:
        # Set up Google API credentials using API key
        api_key = os.environ["GOOGLE_API_KEY"]  # Replace with your actual API key
        youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
        request = youtube.videos().list(part="id,snippet",
                                        id=video_id
                                        )
        response = request.execute()
        title = response['items'][0]['snippet']['title']
        description = response['items'][0]['snippet']['description']
        data = {"title": title, "chapters": parse_chapters(description)}
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

if __name__ == '__main__':
    # Download NLTK punkt resource if not already present
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')

    parser = argparse.ArgumentParser(description='Extract transcript from a YouTube video.')
    parser.add_argument('url', type=str, help='YouTube video URL')
    parser.add_argument('-l', '--language', type=str, default='en', help='Language of the transcript (default: en)')
    parser.add_argument('-r', '--raw', action='store_true', help='Generate raw transcript (default)')
    parser.add_argument('-p', '--punctuated', action='store_true', help='Generate punctuated transcript')
    parser.add_argument('-o', '--output', type=str, help='Output directory for the transcript file')
    parser.add_argument('-f', '--filename', type=str, help='Filename for the transcript file (excluding extension)')
    parser.add_argument('-b', '--batch_size', type=int, default=0,
                        help='User-defined batch size for parallel processing (default: automatic)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose mode')
    parser.add_argument('--punctuation_model', type=str, default='', help='Text for the punctuation model')
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)

    if not args.raw and not args.punctuated:
        args.punctuated = False  # Default to generating raw transcript if no option is specified
    if not args.url:
        parser.error("Please provide a YouTube video URL.")
    # make output directory if not present
    if args.output and not os.path.exists(args.output):
        os.makedirs(args.output, exist_ok=True)
        logging.info(f"Created output directory: {args.output}")

    main()
