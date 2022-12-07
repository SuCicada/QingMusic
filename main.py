from datetime import datetime
import os
import time

import eyed3
from eyed3 import AudioFile
from eyed3.core import Tag
from mutagen.mp3 import MP3, EasyMP3
from mutagen.easyid3 import EasyID3
import csv

# audiofile = eyed3.load("song.mp3")
# audiofile.tag.artist = "Token Entry"
# audiofile.tag.album = "Free For All Comp LP"
# audiofile.tag.album_artist = "Various Artists"
# audiofile.tag.title = "The Edge"
# audiofile.tag.track_num = 3

all_music = "/Users/peng/Music/All"
out_music = "/Users/peng/Music/good"
# all_music = "/Users/peng/Music/test/M-2022"
# out_music = "/Users/peng/Music/test/out/"

overwrite = False

out = open("out.txt", "w")
res = []
dir_sum = {}
summary = {
    "all": 0,
    "good": [],
    "bad": []
}
res_music = []


class Music():
    name: str
    path: str
    dir: str
    date: datetime
    artist: str
    album: str
    title: str
    is_update: bool = False
    tag: Tag


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
    return suffix in ["mp3"]


def get_out_dir(music: Music):
    year = music.date.year
    return os.path.join(out_music, str(year))


def scan(dir):
    for ff in os.listdir(dir):
        f = os.path.join(dir, ff)
        # print(f)
        if os.path.isdir(f):
            scan(f)
        else:
            # is not music
            if not filter_suffix(f):
                continue
            name = get_filename(ff)
            date = get_create_time(f)
            music = Music()
            music.path = f
            music.name = name
            music.date = date
            music.dir = dir
            summary["all"] += 1
            if dir not in dir_sum:
                dir_sum[dir] = 0
            dir_sum[dir] += 1

            audio_file = eyed3.load(f)
            # error type
            if audio_file is None or audio_file.tag is None:
                summary["bad"].append(f)

            else:
                music.tag = audio_file.tag

                # good
                artist = get_artist(audio_file)
                music.artist = artist
                music.title = get_title(audio_file)

                if artist is None:
                    train_music(music)

            res_music.append(music)


def to_csv():
    res_music_dict = []
    for m in res_music:
        delattr(m, 'tag')
        r = vars(m)
        res_music_dict.append(r)

    with open("out.csv", 'w', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=[
            'name', 'title', 'artist', 'date', 'dir', 'path', 'is_update']
                                )
        writer.writeheader()
        writer.writerows(res_music_dict)


artist_libray = ['洛天依', '言和', '鏡音リン・レン', 'JUSF周存', '初音ミク']


def train_music(music: Music):
    try:
        arr = music.name.split("-")
        if len(arr) == 2:
            pre_artist = arr[0].strip()
            pre_title = arr[1].strip()

            music.artist = pre_artist
            music.title = pre_title
            music.tag.artist = music.artist
            music.tag.title = music.title

            music.is_update = True
    except:
        print("error", music.path)
        import traceback
        traceback.print_exc()


import shutil


def save_one_music(music: Music):
    try:
        out = get_out_dir(music)
        if not os.path.exists(out):
            os.makedirs(out)
        dst = os.path.join(out, os.path.basename(music.path))
        if overwrite or not os.path.exists(dst):
            shutil.copy2(music.path, out)
            if music.is_update:
                music.tag.save()
                tt = music.date.timestamp()
                # recover file origin date
                os.utime(music.path, (tt, tt))
    except:
        print("error", music.path)
        import traceback
        traceback.print_exc()


def save_all():
    for i in range(len(res_music)):
        music = res_music[i]
        save_one_music(music)
        print(f"save {i+1}/{len(res_music)}")


scan(all_music)

print("all", summary["all"])
print("good", len(summary["good"]))
print("bad", len(summary["bad"]))
print("need", len(res))
for k, v in dir_sum.items():
    print(k, v)

# to_csv()
save_all()
