import os
import time

import eyed3
from eyed3 import AudioFile
from eyed3.core import Tag

# audiofile = eyed3.load("song.mp3")
# audiofile.tag.artist = "Token Entry"
# audiofile.tag.album = "Free For All Comp LP"
# audiofile.tag.album_artist = "Various Artists"
# audiofile.tag.title = "The Edge"
# audiofile.tag.track_num = 3

Music = "/Users/peng/Music/All"
out = open("out.txt", "w")
res = []
dir_sum = {}
summary = {
    "good": [],
    "bad": []
}


def str_not_blank(s):
    # print(s)
    return s is not None and \
           type(s) is str and \
           len(str(s).strip()) > 0


def has_artist(audio_file: AudioFile):
    tag: Tag = audio_file.tag
    # print(audio_file.path)
    if tag is not None and str_not_blank(tag.artist):
        return True
    return False

def format_time(timestamp):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))

def get_create_time(file_name):
    return format_time(os.path.getmtime(file_name))

def train_music(music):
    audio_file = eyed3.load(music)
    if audio_file is None:
        print("error", music)
    else:
        has_artist(audio_file)


def filter_suffix(file_name):
    suffix = os.path.splitext(file_name)[-1][1:]
    return suffix in ["mp3"]


def scan(dir):
    for ff in os.listdir(dir):
        f = os.path.join(dir, ff)
        # print(f)
        if os.path.isdir(f):
            scan(f)
        else:
            # invalid
            if not filter_suffix(f):
                continue

            audio_file = eyed3.load(f)
            # error type
            if audio_file is None:
                summary["bad"].append(f)
                continue

            # good
            if has_artist(audio_file):
                summary["good"].append(f)
                continue




            if dir not in dir_sum:
                dir_sum[dir] = 0
            dir_sum[dir] += 1
            # d = os.path.dirname(file)
            train_music(f)
            data = {
                "file": f,
                "data": ff,
            }
            res.append(data)


scan(Music)

print("good", len(summary["good"]))
print("bad", len(summary["bad"]))
print("need", len(res))
for k, v in dir_sum.items():
    print(k, v)
for s in res:
    out.write(s)
    out.write("\r\n")
