import argparse

import webvtt
from yt_dlp import YoutubeDL

# Setup to extract only subtitles without downloading the video itself.
YDL_OPTIONS = {
    "skip_download": True,
    "writeautomaticsub": True,
}


# Set command line arguments
def init_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="Youtube video link to download subtitles")
    argument = parser.parse_args()
    return argument


# Download subtitle files and obtain meta information.
def get_video_info(url):
    with YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url)

    return info


# Extract only the text from the subtitle vvt file.
def get_caption(video_info):
    subtitle_file_name = video_info["requested_subtitles"]["en"]["filepath"]
    vtt = webvtt.read(subtitle_file_name)
    captions_duplicated = [caption.text for caption in vtt]

    captions = []

    for caption in captions_duplicated:
        texts = caption.split('\n')

        for text in texts:
            captions.append(text)

    captions = list(dict.fromkeys(captions))

    all_text = " ".join(captions)
    return all_text


if __name__ == '__main__':
    args = init_argument()
    url = args.url

    video_info = get_video_info(url)
    subtitles = get_caption(video_info)

    video_title = video_info["title"]

    with open(f"{video_title}_sub.txt", "w") as f:
        f.write(subtitles)
