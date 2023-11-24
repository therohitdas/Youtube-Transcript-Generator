# YouTube Transcript Generator
[![Open in Collab](https://img.shields.io/badge/Open_in_Collab-555?style=for-the-badge&logo=googlecolab&labelColor=gray&color=purple)](https://colab.research.google.com/github/therohitdas/Youtube-Transcript-Generator/blob/main/main.ipynb)
![GitHub License](https://img.shields.io/github/license/therohitdas/Youtube-Transcript-Generator?style=for-the-badge&color=blue) ![GitHub Repo stars](https://img.shields.io/github/stars/therohitdas/Youtube-Transcript-Generator?style=for-the-badge&logo=github)

## Overview 🌐

The YouTube Transcript Generator is a powerful tool designed to streamline the process of extracting and processing transcripts from YouTube videos. Whether you're looking to transcribe lectures, interviews, or any other video content, this project provides a convenient solution.

### How It Can Help 🚀

This tool is particularly useful for:
- **Note Taking:** Quickly convert YouTube videos into text format for easy note-taking.
- **Content Analysis:** Analyze and derive insights from video content by converting it into text data.
- **Chat Bot Training:** Use the generated transcripts to train chatbots, such as ChatGPT, for natural language understanding.
- **Archiving:** Create a textual archive of valuable information from YouTube videos. This can be particularly useful for archiving interviews, tutorials, or any content you'd like to reference later without the need to re-watch the video.
- **Personal Knowledge Base:** Build a personal knowledge base by extracting and processing transcripts from YouTube videos. This can aid in consolidating information on diverse topics in a readable and accessible format.
- **Accessibility Improvement:** Enhance accessibility for individuals who prefer or require text-based content. The tool can be used to generate transcripts with added punctuation, improving the overall readability of the content.

## Features 🛠️

- **Transcription:** Obtain raw transcripts from YouTube videos.
- **Punctuation:** Enhance transcripts by adding punctuation using [deep multilingual punctuation models](https://huggingface.co/oliverguhr/fullstop-punctuation-multilang-large).
- **Chapter Detection:** Identify and separate chapters in the video based on provided timestamps.
- **User-friendly:** Easy-to-use script with customizable parameters.

## Environment Variables 🌐

- `GOOGLE_API_KEY`: Set up your Google API key for video information retrieval. You will need to create a Project in the Google Cloud for this and enable the YouTube v3 API. This is optional, if you don't add it, the chapters will not be added.

## Script Parameters 📜
When running the script locally, you can pass these parameters to the script:

### Positional Argument:
- `url`: YouTube video URL

### Optional Arguments:
- `-h, --help`: Show the help message and exit
- `-l LANGUAGE, --language LANGUAGE`: Language for the transcript (default: en)
- `-p, --punctuated`: Generate punctuated transcript (default: False)
- `-o OUTPUT_DIR, --output_dir OUTPUT_DIR`: Output directory for saving the transcript (default: .)
- `-f FILENAME, --filename FILENAME`: Filename for saving the transcript (default: Video Title or Video Id)
- `-m PUNCTUATION_MODEL, --punctuation_model PUNCTUATION_MODEL`: Path to the punctuation model (default: None)
- `-v, --verbose`: Print verbose output (default: False)

## Run in Google Collab 🚀
To run this project in Google Colab, follow these steps:
1. Open the [Google Colab notebook](https://colab.research.google.com/github/therohitdas/Youtube-Transcript-Generator/blob/main/main.ipynb).
2. Add Google's Project API key to the secrets tab under this key: `GOOGLE_API_KEY` and toggle notebook access to on.
3. Edit the variables in the second last cell.
4. Go to Runtime > Change Runtime Type and select any GPU type. If you use CPU, the output for punctuated transcript will take some minutes to complete (around 1 minute per 10-minute video)
5. Change the values in the third last cell to include your URL etc.

## Run Locally 💻

I do not recommend running locally as it will download tensors and other stuff which are over 6gb. But if you want you can do this:
1. Clone the repository: `git clone https://github.com/therohitdas/Youtube-Transcript-Generator.git`
2. Install dependencies: `pip install youtube-transcript-api deepmultilingualpunctuation nltk tqdm pip install google-api-python-client google-auth-oauthlib`
3. Set up the required environment variables: `GOOGLE_API_KEY` (optional).
4. Run the script: `python index.py <YouTube_URL>` or `python index.py -h` for the help menu.

## Support 🤝

For any issues or feature requests, please [create an issue](https://github.com/therohitdas/Youtube-Transcript-Generator/issues).

## Example 📋
Here's an example of how to run the script with various options:

### Basic Usage
```bash
python index.py https://www.youtube.com/watch?v=VIDEO_ID
```

### Specify the Language

```bash
python index.py https://www.youtube.com/watch?v=VIDEO_ID -l fr
```

### Generate a Raw Transcript

```bash
python index.py https://www.youtube.com/watch?v=VIDEO_ID
```

### Generate a Punctuated Transcript

```bash
python index.py https://www.youtube.com/watch?v=VIDEO_ID -p
```

### Specify the Output Directory

```bash
python index.py https://www.youtube.com/watch?v=VIDEO_ID -o /path/to/output
```

### Specify a Custom Filename

```bash
python index.py https://www.youtube.com/watch?v=VIDEO_ID -f custom_filename
```

### Enable Verbose Mode

```bash
python index.py https://www.youtube.com/watch?v=VIDEO_ID -v
```

### Specify a Punctuation Model

```bash
python index.py https://www.youtube.com/watch?v=VIDEO_ID -m author/model_name
```
Punctuation model name can be taken from [here](https://huggingface.co/oliverguhr/fullstop-punctuation-multilang-large#languages).

Make sure to replace `https://www.youtube.com/watch?v=VIDEO_ID` with the actual URL of the YouTube video you want to process.

Feel free to copy and paste these examples into your terminal.
## Acknowledgments 🙌

This script utilizes the [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api) and [fullstop-punctuation-multilang-large](https://huggingface.co/oliverguhr/fullstop-punctuation-multilang-large) libraries. Special thanks to their contributors.

Feel free to adapt and use the script based on your requirements. Enjoy the convenience of YouTube transcript processing!

## Connect with me 📧
The best way to connect is to email me [namaste@theRohitDas.com](mailto:namaste@therohitdas.com)
- [x/therohitdas](https://x.com/therohitdas)
- [GitHub/therohitdas](https://github.com/therohitdas)

🚀 Happy transcribing!
