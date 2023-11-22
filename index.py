import argparse
import os
import youtube_transcript_api
from deepmultilingualpunctuation import PunctuationModel
from nltk import sent_tokenize
from multiprocessing import Pool
import time
import logging
from tqdm import tqdm
import re
import math
import nltk

# Download NLTK punkt resource if not already present
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

logging.basicConfig(level=logging.INFO)

def get_transcript(video_id, language):
    transcript_list = youtube_transcript_api.YouTubeTranscriptApi.get_transcript(video_id, languages=[language])
    transcript = ''
    for line in transcript_list:
        transcript += line['text'] + ' '
    return transcript

def add_punctuation(text, punctuation_model):
    if punctuation_model != "":
        model = PunctuationModel(model=punctuation_model)
    else:
        model = PunctuationModel()
    return model.restore_punctuation(text)

def capitalize_sentences_batch(sentences):
    # Capitalize the first letter of each sentence in a batch
    capitalized_sentences = [sentence[0].upper() + sentence[1:] for sentence in sentences]
    return capitalized_sentences

def process_and_save_transcript(video_id, language, generate_punctuated, output_dir, filename, batch_size, verbose, punctuation_model):
    try:
        raw_transcript = get_transcript(video_id, language)

        if generate_punctuated:
            with_punctuation = add_punctuation(raw_transcript, punctuation_model)
            sentences = sent_tokenize(with_punctuation)
            num_processes = os.cpu_count() or 1  # Get the number of available processes
            batch_size = 2**int(math.log2(batch_size)) if batch_size else num_processes  # Restrict batch size to be a power of 2, default to number of cores
            with Pool() as pool:
                capitalized_sentences = list(tqdm(pool.imap(capitalize_sentences_batch, [sentences[i:i+batch_size] for i in range(0, len(sentences), batch_size)]), total=len(sentences), desc='Processing', disable=not verbose))
            capitalized_transcript = ' '.join([sentence for batch in capitalized_sentences for sentence in batch])
            output_path = os.path.join(output_dir, f'{filename}_punctuated.txt')
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(capitalized_transcript)
            logging.info(f'Punctuated transcript saved to {output_path}')
        else:
            sentences = sent_tokenize(raw_transcript)
            num_processes = os.cpu_count() or 1  # Get the number of available processes
            batch_size = 2**int(math.log2(batch_size)) if batch_size else num_processes  # Restrict batch size to be a power of 2, default to number of cores
            with Pool() as pool:
                capitalized_sentences = list(tqdm(pool.imap(capitalize_sentences_batch, [sentences[i:i+batch_size] for i in range(0, len(sentences), batch_size)]), total=len(sentences), desc='Processing', disable=not verbose))
            capitalized_transcript = ' '.join([sentence for batch in capitalized_sentences for sentence in batch])
            output_path = os.path.join(output_dir, f'{filename}_raw.txt')
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

def main():
    parser = argparse.ArgumentParser(description='Extract transcript from a YouTube video.')
    parser.add_argument('url', type=str, help='YouTube video URL')
    parser.add_argument('-l', '--language', type=str, default='en', help='Language of the transcript (default: en)')
    parser.add_argument('-r', '--raw', action='store_true', help='Generate raw transcript (default)')
    parser.add_argument('-p', '--punctuated', action='store_true', help='Generate punctuated transcript')
    parser.add_argument('-o', '--output', type=str, help='Output directory for the transcript file')
    parser.add_argument('-f', '--filename', type=str, help='Filename for the transcript file (excluding extension)')
    parser.add_argument('-b', '--batch_size', type=int, default=0, help='User-defined batch size for parallel processing (default: automatic)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose mode')
    parser.add_argument('--punctuation_model', type=str, default='', help='Text for the punctuation model')
    args = parser.parse_args()

    if not args.raw and not args.punctuated:
        args.raw = True  # Default to generating raw transcript if no option is specified

    video_id = parse_youtube_url(args.url)

    language = args.language or "en"
    
    output_dir = args.output or os.getcwd()
    filename = args.filename or f'{video_id}_raw'  # Default filename if not provided
    batch_size = args.batch_size or 0  # 0 will automatically determine batch size

    process_and_save_transcript(video_id, language, args.punctuated, output_dir, filename, batch_size, args.verbose, args.punctuation_model)

if __name__ == '__main__':
    main()
