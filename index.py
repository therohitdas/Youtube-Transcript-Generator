import os
import argparse
import logging
import re
import math
import warnings
import subprocess
import platform

from tqdm import tqdm
from rpunct import RestorePuncts
import googleapiclient.discovery
import googleapiclient.errors
from youtube_transcript_api import YouTubeTranscriptApi

verbose = logging.ERROR
logging.basicConfig(level=verbose, force=True)

# stop any warnings
warnings.filterwarnings("ignore")


def open_file(filename):
    # Open the file using the default application
    logging.info(f"Opening \"{filename}\"...")
    try:
        if platform.system() == "Darwin":       # macOS
            subprocess.call(("open", filename))
        elif platform.system() == "Windows":    # Windows
            os.startfile(filename)
        else:                                   # linux variants
            subprocess.call(("xdg-open", filename))
    except Exception as e:
        logging.error(f"Error: {e}")


def clean_for_filename(title):
    """
    Define a regular expression to keep only alphanumeric characters, spaces,
    dots, hyphens, and various parentheses
    """
    cleaned_title = re.sub(r"[^\w\s\.\-\(\)\[\]]", "", title)

    # Remove leading and trailing spaces
    return cleaned_title.strip()


def remove_tags(text):
    # Remove any text inside [] like [music]
    updated_text = re.sub(r"\[.*?\]", "", text)
    return updated_text


def remove_escape_sequences(text):
    # Some old videos contain escape sequences like \n in their subtitle
    # Remove \n, \r\n, \t, \b, \r
    return re.sub(r"\\[nrtb]|\\r\n", "", text)


def remove_double_greater_than(text):
    # Replace occurrences of ">>" with an empty string
    cleaned_text = re.sub(r">>", "", text)
    return cleaned_text


def improve_readability(text):
    transcript = []
    current_line = ""
    # Loop through each character in the string
    for char in text:
        # Add the character to the current line
        current_line += char
        # If the character is a full stop, question mark, or exclamation mark
        if char in ".?!":
            # Strip leading and trailing whitespace from the current line
            current_line = current_line.strip()
            # If the current line is not empty, add it to the transcript
            if current_line != "":
                transcript.append(current_line)
            # Start a new line
            current_line = ""
    # If the current line is not empty, add it to the transcript
    if current_line.strip() != "":
        transcript.append(current_line.strip())
    return os.linesep.join(transcript)


def add_punctuation(text):
    rpunct = RestorePuncts()
    return rpunct.punctuate(text, lang="en")


def parse_youtube_url(url):
    video_id_match = re.search(
        r'(?:youtube\.com\/.*?[?&]v=|youtu\.be\/)([^"&?\/\s]{11})', url)
    if video_id_match:
        return video_id_match.group(1)
    else:
        raise ValueError("Invalid YouTube URL")


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
            title = re.sub(r"\d{0,2}:?\d{1,2}:\d{2}", "", title).strip().strip(
                "-").strip().strip("-").strip()

            chapters.append({
                "timestamp": ts,
                "title": title,
            })

    return chapters


def get_transcript(video_id, video_info):
    transcript_list = YouTubeTranscriptApi.get_transcript(
        video_id, languages=["en"])
    transcript_array = []
    transcript = ""
    # Add title to the transcript
    if video_info["title"] != "":
        transcript_array.append(
            f"# [{video_info['title']}]({video_info['url']}){os.linesep}"
        )

    current_chapter_index = 0
    chapters = video_info["chapters"]
    logging.info(
        "Found {} chapters and {} lines in the transcript".format(
            len(chapters), len(transcript_list)
        )
    )
    logging.info("Processing transcript...")
    # Process each line in the transcript
    for i, line in enumerate(transcript_list):
        # Floor and convert to integer
        start_time = int(math.floor(line["start"]))

        # Check if current_chapter_index is within the valid range
        if 0 <= current_chapter_index < len(chapters):
            chapter_time = chapters[current_chapter_index]["timestamp"]

            try:
                # Extract start time from the chapter timestamp
                chapter_start = chapter_time.strip()
                chapter_start_seconds = sum(
                    int(x) * 60 ** i
                    for i, x in enumerate(reversed(chapter_start.split(":")))
                )
                chapters[current_chapter_index]["title"] = (
                    chapters[current_chapter_index]["title"].strip()
                )

                if start_time >= chapter_start_seconds:
                    # If the start time is within the buffer time,
                    # Append the accumulated transcript to the transcript array
                    if transcript != "":
                        transcript_array.append(
                            f"{transcript.strip()}"
                        )
                        transcript = ""
                    # Append the chapter title to the transcript array
                    transcript_array.append(
                        "{}## {}{}".format(
                            os.linesep,
                            chapters[current_chapter_index]["title"],
                            os.linesep
                        )
                    )
                    current_chapter_index += 1
            except Exception as e:
                logging.exception(e)

        line["text"] = remove_tags(line["text"])
        line["text"] = remove_escape_sequences(line["text"])
        line["text"] = remove_double_greater_than(line["text"])
        if line["text"]:
            transcript += line["text"] + " "

    # Add the last transcript to the transcript array
    if transcript != "":
        transcript_array.append(
            f"{transcript.strip()}"
        )
    logging.info("Completed processing the transcript")
    return transcript_array


def process_and_save_transcript(
        video_id, video_info, generate_punctuated, output_dir, filename
):
    try:
        logging.info("Getting transcript...")
        raw_transcript = get_transcript(video_id, video_info)

        if generate_punctuated:
            punctuated_transcript = []
            logging.info("Generating punctuated transcript...")
            for i, line in tqdm(enumerate(raw_transcript),
                                total=len(raw_transcript)):
                try:
                    if line.startswith("#"):
                        punctuated_transcript.append(line)
                        continue
                    logging.getLogger().setLevel(logging.ERROR)
                    punctuated_transcript.append(
                        improve_readability(
                            add_punctuation(line)
                        )
                    )

                    logging.getLogger().setLevel(verbose)
                except Exception as e:
                    logging.error(f"Error punctuating line {i+1}")
                    logging.error(
                        "Raw line content: {} and Raw Line length: {}"
                        .format(line, len(line))
                    )
                    logging.exception(e)
                    punctuated_transcript.append(improve_readability(line))
            transcript = punctuated_transcript
            logging.info("Completed punctuating the transcript")
        else:
            transcript = [
                improve_readability(line) for line in raw_transcript
            ]
        doublelinesep = os.linesep+os.linesep
        transcript = doublelinesep.join(transcript)
        output_path = os.path.join(output_dir, f"{filename}.md")

        logging.info(f"Saving transcript to {output_path}...")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(transcript)

        # set log level to info to print the output path
        logging.getLogger().setLevel(logging.INFO)
        if generate_punctuated:
            logging.info(f"Punctuated transcript saved to \"{output_path}\"")
        else:
            logging.info(f"Raw transcript saved to \"{output_path}\"")
        return True
    except Exception as e:
        # log stack trace
        logging.exception(e)
        return False


def getVideoInfo(video_id):
    url = f"https://www.youtube.com/watch?v={video_id}"
    try:
        # Set up Google API credentials using API key
        api_key = os.environ.get("YOUTUBE_API_KEY")
        if api_key is None:
            raise Exception(
                """No API key found\n
                Please set the YOUTUBE_API_KEY environment variable.\n
                Example: export YOUTUBE_API_KEY=your_api_key"""
            )
        logging.info("Getting video info...")
        logging.getLogger().setLevel(logging.ERROR)
        youtube = googleapiclient.discovery.build(
            "youtube", "v3", developerKey=api_key
        )
        request = youtube.videos().list(part="id,snippet",
                                        id=video_id
                                        )
        response = request.execute()
        logging.getLogger().setLevel(verbose)
        title = response["items"][0]["snippet"]["title"]
        description = response["items"][0]["snippet"]["description"]
        data = {
            "title": title,
            "chapters": parse_chapters(description),
            "url": url
        }
        return data
    except Exception as e:
        logging.error(f"Error: {e}")
        return {"title": video_id, "chapters": [], "url": url}


def main():
    parser = argparse.ArgumentParser(
        description="Process YouTube video transcript and save it.")
    parser.add_argument("url", type=str, help="YouTube video URL")
    parser.add_argument("-p", "--punctuated", action="store_true",
                        help="Generate punctuated transcript (default: False)")
    parser.add_argument("-o", "--output_dir", type=str, default=".",
                        help="Output directory (default: .)")
    parser.add_argument("-f", "--filename", type=str, default="",
                        help="Filename (default: Video Title or Video Id)")
    parser.add_argument("-a", "--auto-open", action="store_true",
                        help="Open generated transcript (default: False)")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Print verbose output (default: False)")

    args = parser.parse_args()

    # if verbose is false, set logging level to error
    if args.verbose:
        global verbose
        verbose = logging.INFO
        logging.getLogger().setLevel(verbose)

    video_id = parse_youtube_url(args.url)
    video_info = getVideoInfo(video_id)
    filename = args.filename or clean_for_filename(
        video_info["title"]) or clean_for_filename(video_id)

    status = process_and_save_transcript(video_id, video_info, args.punctuated,
                                         args.output_dir, filename)

    if status and args.auto_open:
        output_path = os.path.join(args.output_dir, f"{filename}.md")
        open_file(output_path)


if __name__ == "__main__":
    main()
