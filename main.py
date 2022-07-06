import argparse
import os

import deepl
import webvtt
from yt_dlp import YoutubeDL

USE_DEEPL = True

# Setup to extract only subtitles without downloading the video itself.
YDL_OPTIONS = {
    "skip_download": True,
    "writeautomaticsub": True,
}

# DeepL Set the KEY for the API
DEEPL_API_KEY = os.environ["DEEPL_API_KEY"]

# Setting up languages to be translated at DeepL
SOURCE_LANG = 'EN'
TARGET_LANG = 'JA'


# Set command line arguments
def init_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="Youtube video link to download subtitles")
    argument = parser.parse_args()
    return argument


# Download subtitle files and obtain meta information.
def get_video_info(url):
    os.chdir("./output/vtt")
    with YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url)
    
    os.chdir("../../")
    return info


# Extract only the text from the subtitle vvt file.
def get_caption(video_info):
    subtitle_file_name = video_info["requested_subtitles"]["en"]["filepath"]
    vtt = webvtt.read(f"output/vtt/{subtitle_file_name}")
    captions_duplicated = [caption.text for caption in vtt]

    captions = []

    for caption in captions_duplicated:
        texts = caption.split('\n')

        for text in texts:
            captions.append(text)

    captions = list(dict.fromkeys(captions))

    all_text = " ".join(captions)
    return all_text


def main():
    args = init_argument()
    url = args.url

    video_info = get_video_info(url)
    subtitles_en = get_caption(video_info)

    video_title = video_info["title"]

    # translate en -> ja
    if USE_DEEPL:
        translator = deepl.Translator(DEEPL_API_KEY)
        subtitles_ja = translator.translate_text(
            text=subtitles_en,
            source_lang=SOURCE_LANG,
            target_lang=TARGET_LANG,
        )

        with open(f"output/txt/{video_title}_sub.txt", "w") as f:
            f.write(str(subtitles_ja))
    else:
        with open(f"output/txt/{video_title}_sub.txt", "w") as f:
            f.write(str(subtitles_en))


if __name__ == '__main__':
    main()
