from datetime import datetime
import os
import time

import eyed3
from eyed3 import AudioFile
from eyed3.core import Tag
from mutagen.mp3 import MP3, EasyMP3
from mutagen.easyid3 import EasyID3
import csv
def str_not_blank(s):
    # print(s)
    return s is not None and \
        type(s) is str and \
        len(str(s).strip()) > 0


def get_tag_value(audio_file: AudioFile, key: str):
    tag: Tag = audio_file.tag
    if tag is not None:
        v = getattr(tag, key)
        if str_not_blank(v):
            return v
    return None


def get_artist(audio_file: AudioFile):
    return get_tag_value(audio_file, 'artist')



def get_title(audio_file: AudioFile):
    return get_tag_value(audio_file, 'title')


def has_artist(audio_file: AudioFile):
    return get_artist(audio_file) is not None


def format_time(timestamp):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))


def get_create_time(file_name) -> datetime:
    timestamp = os.path.getmtime(file_name)
    return datetime.fromtimestamp(timestamp)


def get_filename(file_name):
    return os.path.splitext(file_name)[0]


def get_suffix(file_name):
    return os.path.splitext(file_name)[-1][1:]


def filter_suffix(file_name):
    suffix = get_suffix(file_name)
    return suffix.lower() in ["mp3","flac"]
