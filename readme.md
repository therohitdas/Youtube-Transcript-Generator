# YouTube Transcript Generator

[![Open in Colab](https://img.shields.io/badge/Open_in_Colab-555?style=for-the-badge&logo=googlecolab&labelColor=gray&color=purple)](https://colab.research.google.com/github/therohitdas/Youtube-Transcript-Generator/blob/main/main.ipynb)
![GitHub License](https://img.shields.io/github/license/therohitdas/Youtube-Transcript-Generator?style=for-the-badge&color=blue) ![GitHub Repo stars](https://img.shields.io/github/stars/therohitdas/Youtube-Transcript-Generator?style=for-the-badge&logo=github)
[![CodeFactor](https://www.codefactor.io/repository/github/therohitdas/youtube-transcript-generator/badge?style=for-the-badge)](https://www.codefactor.io/repository/github/therohitdas/youtube-transcript-generator)

## Overview 🌐

The YouTube Transcript Generator is a powerful tool designed to streamline the process of extracting and processing transcripts from YouTube videos. Whether you're looking to transcribe lectures, interviews, or any other video content, this project provides a convenient solution.

### Variant:

This script uses a fork of [rpunct by Daulet Nurmanbetov](https://github.com/therohitdas/rpunct) for punctuating the text. This variant is more accurate but takes longer to run.
If you want to use the other version, use the main branch of my repo.

### How It Can Help 🚀

This tool is particularly useful for:

- **Note Taking:** Quickly convert YouTube videos into text format for easy note-taking.
- **Content Analysis:** Analyze and derive insights from video content by converting it into text data.
- **Chat Bot Training:** Use the generated transcripts to train chat bots, such as ChatGPT, for natural language understanding.
- **Archiving:** Create a textual archive of valuable information from YouTube videos. This can be particularly useful for archiving interviews, tutorials, or any content you'd like to reference later without the need to re-watch the video.
- **Personal Knowledge Base:** Build a personal knowledge base by extracting and processing transcripts from YouTube videos. This can aid in consolidating information on diverse topics in a readable and accessible format.
- **Accessibility Improvement:** Enhance accessibility for individuals who prefer or require text-based content. The tool can be used to generate transcripts with added punctuation, improving the overall readability of the content.

## Features 🛠️

- **Transcription:** Obtain raw transcripts from YouTube videos.
- **Punctuation:** Enhance transcripts by adding punctuation using [felflare/bert-restore-punctuation](https://huggingface.co/felflare/bert-restore-punctuation).
- **Chapter Detection:** Identify and separate chapters in the video based on provided timestamps.
- **User-friendly:** Easy-to-use script with customizable parameters.

## Environment Variables 🌐

- `YOUTUBE_API_KEY`: Set up your Google API key for video information retrieval. You will need to create a Project in the Google Cloud for this and enable the YouTube v3 API. This is optional, if you don't add it, the chapters will not be added.

## Script Parameters 📜

When running the script locally, you can pass these parameters to the script:

### Positional Argument:

- `url`: YouTube video URL

### Optional Arguments:

- `-h, --help`: Show the help message and exit
- `-p, --punctuated`: Generate punctuated transcript (default: False)
- `-a, -auto-open`: Automatically open the transcript in the default app (default: False)
- `-o OUTPUT_DIR, --output_dir OUTPUT_DIR`: Output directory for saving the transcript (default: current directory)
- `-f FILENAME, --filename FILENAME`: Filename for saving the transcript (default: Video Title or Video Id)
- `-v, --verbose`: Print verbose output (default: False)

<!-- ## Run in Google Colab 🚀

To run this project in Google Colab, follow these steps:

1. Open the [Google Colab Notebook](https://colab.research.google.com/github/therohitdas/Youtube-Transcript-Generator/blob/main/main.ipynb).
2. Add Google's Project API key to the secrets tab under this key: `YOUTUBE_API_KEY` and toggle notebook access to on.
3. Go to Runtime > Change Runtime Type and select T4 GPU type. If you use CPU, the output for punctuated transcript will take some minutes to complete (around 1 minute per 10-minute video)
4. Change the values in the second cell to include your URL etc.
5. Press CTRL+F9 or CMD+F9 to run the notebook. -->

## Run Locally 💻

1. Clone the repository:

```bash
git clone -b bert https://github.com/therohitdas/Youtube-Transcript-Generator.git && cd Youtube-Transcript-Generator
```

2. Create a virtual environment:

```bash
python -m venv venv
```

3. Activate the virtual environment:

```bash
source venv/bin/activate #(Linux/MacOS)
# or
venv\Scripts\activate #(Windows)
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Set up the required environment variables: `YOUTUBE_API_KEY` (optional). You can either create a `.env` file or set them up in your system using.
6. Run the script:

```bash
python index.py <YouTube_URL> -p -v
# or
python index.py <YouTube_URL> -h # for help
```

> ❗️ **Important:** The first run can be slow as the model is downloaded. Please run in verbose mode to see the progress. If the script appears to be stuck, please wait for a few minutes before terminating the process.

## Support 🤝

For any issues or feature requests, please [create an issue](https://github.com/therohitdas/Youtube-Transcript-Generator/issues).

## Example 📋

Here's an example of how to run the script with various options:

### Basic Usage

```bash
python index.py https://www.youtube.com/watch?v=VIDEO_ID
```

### My favorite usage

Generates punctuated transcript, adds chapters and opens the transcript in the default app.

```bash
python index.py https://www.youtube.com/watch?v=VIDEO_ID -pav -o ~/Documents/Transcripts
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

### Automatically Open the Transcript

```bash
python index.py https://www.youtube.com/watch?v=VIDEO_ID -a
```

Make sure to replace `https://www.youtube.com/watch?v=VIDEO_ID` with the actual URL of the YouTube video you want to process.

Feel free to copy and paste these examples into your terminal.

## Acknowledgments 🙌

This script utilizes the [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api) and forked [rpunct](https://github.com/therohitdas/rpunct) libraries. Special thanks to their contributors.

Feel free to adapt and use the script based on your requirements. Enjoy the convenience of YouTube transcript processing!

## Connect with me 📧

The best way to connect is to email me [namaste@theRohitDas.com](mailto:namaste@therohitdas.com)

- [x/therohitdas](https://x.com/therohitdas)
- [GitHub/therohitdas](https://github.com/therohitdas)

🚀 Happy transcribing!
