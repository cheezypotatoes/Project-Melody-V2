from pytube import YouTube
from moviepy.editor import VideoFileClip
import sys
import os
import requests


def download(link, thumbnail_directory, mp3_directory):
    output = open("output.txt", "wt")
    sys.stdout = output
    sys.stderr = output

    link_for_yt = link

    # initializing
    yt = YouTube(link_for_yt)
    thumbnail_url = yt.thumbnail_url
    audio = yt.streams.get_highest_resolution()

    # getting the titles and removing some characters
    title = yt.title
    invalid_chars = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
    valid_title = ''.join(char for char in title if char not in invalid_chars)

    # downloads the mp4 and convert
    video_file_path = audio.download()
    video = VideoFileClip(video_file_path)
    audio_file_path = fr"{mp3_directory}\{valid_title}.mp3"
    video.audio.write_audiofile(audio_file_path)

    # initializing the thumbnails
    save_path = os.path.join(thumbnail_directory, valid_title + ".png")
    response = requests.get(thumbnail_url)

    # downloading the thumbnail
    with open(save_path, "wb") as f:
        f.write(response.content)

    video.close()
    os.remove(video_file_path)

    print(thumbnail_directory)
    print(mp3_directory)










