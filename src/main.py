from datetime import datetime
import os
import time

import eyed3
from eyed3 import AudioFile
from eyed3.core import Tag
from mutagen.mp3 import MP3, EasyMP3
from mutagen.easyid3 import EasyID3
import csv

from src.fix import fix_music
from src.music import *
from src.type import Music

# audiofile = eyed3.load("song.mp3")
# audiofile.tag.artist = "Token Entry"
# audiofile.tag.album = "Free For All Comp LP"
# audiofile.tag.album_artist = "Various Artists"
# audiofile.tag.title = "The Edge"
# audiofile.tag.track_num = 3

# all_music = "/Users/peng/Music/All"
# out_music = "/Users/peng/Music/good"
all_music = "/Users/peng/Music/All"
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


def get_out_dir(music: Music):
    year = music.date.year
    return os.path.join(out_music, str(year))


def scan(dir) -> [Music]:
    _res_music = []
    def sub_scan(dir) -> [Music]:
        for ff in os.listdir(dir):
            f = os.path.join(dir, ff)
            # print(f)
            if os.path.isdir(f):
                sub_scan(f)
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
                    music.is_good = False
                    summary["bad"].append(f)

                else:
                    music.tag = audio_file.tag

                    # good
                    music.title = get_title(audio_file)
                    artist = get_artist(audio_file)

                    if artist is not None:
                        music.artist = artist
                    else:
                        fix_music(music)

                _res_music.append(music)
    sub_scan(dir)
    return _res_music


def to_csv(res_music: [Music]):
    res_music_dict = []
    for m in res_music:
        try:
            if hasattr(m, "tag"):
                delattr(m, 'tag')
            r = vars(m)
            res_music_dict.append(r)

        except:
            print("error", m.tag)
            import traceback
            traceback.print_exc()

    with open("out.csv", 'w', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=[
            'name', 'title', 'artist', 'date', 'dir', 'path', 'is_update', 'is_good'
        ])
        writer.writeheader()
        writer.writerows(res_music_dict)

artist_libray = ['洛天依', '言和', '鏡音リン・レン', 'JUSF周存', '初音ミク']



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
        print(f"save {i + 1}/{len(res_music)}")


if __name__ == '__main__':
    res_music = scan(all_music)
    print("all", len(res_music))
    print("good", len(summary["good"]))
    print("bad", len(summary["bad"]))
    print("need", len(res))
    for k, v in dir_sum.items():
        print(k, v)
    to_csv(res_music)
    # save_all()
