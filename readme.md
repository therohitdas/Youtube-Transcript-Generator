# YouTube Transcript Processing Tool

## Overview

This repository contains a versatile script for extracting and enhancing transcripts from YouTube videos. The script utilizes the [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api) for obtaining raw transcripts and the [fullstop-punctuation-multilang-large](https://huggingface.co/oliverguhr/fullstop-punctuation-multilang-large) model for adding punctuations.

## Features

- **Raw Transcript Extraction:** Obtain raw transcripts from YouTube videos, supporting both auto-generated and user-added subtitles.

- **Punctuation Enhancement:** Improve transcript readability by adding punctuations using a powerful multilingual punctuation model.

## Usecase

### Note Taking

Effortlessly transcribe and enhance YouTube video content, making it convenient for note-taking during educational lectures, seminars, or any content you wish to remember.

### Archiving

Create a textual archive of valuable information from YouTube videos. This can be particularly useful for archiving interviews, tutorials, or any content you'd like to reference later without the need to re-watch the video.

### Training Data for Machine Learning

Gather high-quality training data for machine learning projects that involve natural language processing (NLP) or speech recognition. The tool provides a streamlined way to obtain clean and punctuated transcripts for model training.

### Personal Knowledge Base

Build a personal knowledge base by extracting and processing transcripts from YouTube videos. This can aid in consolidating information on diverse topics in a readable and accessible format.

### Accessibility Improvement

Enhance accessibility for individuals who prefer or require text-based content. The tool can be used to generate transcripts with added punctuations, improving the overall readability of the content.

Feel free to explore additional use cases based on your specific needs and requirements! Suggest more use cases using issues or private DM on twitter.

## Requirements

Ensure you have the following dependencies installed:

- [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api)
- [fullstop-punctuation-multilang-large](https://huggingface.co/oliverguhr/fullstop-punctuation-multilang-large)
- nltk
- tqdm

## Usage Options

This tool can be utilized in two ways:

### 1. Google Colab Notebook (Recommended)

- Open the [Google Colab notebook](https://colab.research.google.com/github/therohitdas/Youtube-Transcript-Generator/blob/main/main.ipynb).
- Click on **File > Save a copy in Drive** to create your version.
- Adjust script parameters in the notebook.
- Execute the script cell to process the YouTube video transcript.

### 2. Local Execution Using Python Script

- Install Dependencies `pip install youtube-transcript-api deepmultilingualpunctuation nltk tqdm`
- Run the provided Python script `script.py` locally on your machine.
- Supply the required command-line arguments for customization.
- Example:
  ```bash
  python script.py --url 'https://www.youtube.com/watch?v=YOUR_VIDEO_ID' --language 'en' --raw --output '/content' --filename 'notes'
  ```

## Script Parameters

- `url`: YouTube video URL. Both url formats are supported.
- `language`: Language of the transcript (default: en).
- `raw`: Generate raw transcript (default: True).
- `punctuated`: Generate punctuated transcript.
- `output`: Output directory for the transcript.
- `filename`: Filename for the transcript file (excluding extension).
- `batch_size`: Batch size for parallel processing (default: 0, auto-detect based on CPU cores).
- `verbose`: Enable verbose mode for detailed output (default: True).
- `punctuation_model`: Text for the punctuation model (default: '').
  Every parameter is optional except URL

## Acknowledgments

This script utilizes the [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api) and [fullstop-punctuation-multilang-large](https://huggingface.co/oliverguhr/fullstop-punctuation-multilang-large) libraries. Special thanks to their contributors.

Feel free to adapt and use the script based on your requirements. Enjoy the convenience of YouTube transcript processing!

## Connect with me

I am new to the AI world and would love to connect with others who share this interest.

- [x/therohitdas](https://x.com/therohitdas)
- [GitHub/therohitdas](https://github.com/therohitdas)
