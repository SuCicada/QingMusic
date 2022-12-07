import os.path
import time
import os
from pprint import pprint
from eyed3.core import Tag

import eyed3

from main import get_create_time

music = "test.mp3"
from mutagen.flac import FLAC
from mutagen.mp3 import MP3, EasyMP3
from mutagen.easyid3 import EasyID3

# for k,v in EasyMP3.ID3.valid_keys.items():
#     print(k,v)

audio = MP3(music)
tags = EasyID3(music)
tags['title'] = 'new_title'
tags['artist'] = tags['composer'] = 'memememe'
tags['date'] = '2020-03-22'
# tags['command'] = '2020-03-22'
# print(audio)
for key, value in tags.items():
    print(key, ":", value[0])
print("===========================-")
# tags.save()
# audio.ta
# audio["title"] = u"An example"
pprint(audio.info.pprint())


def get_info(music):
    create_time = os.path.getmtime(music)
    m = eyed3.load(music)
    print(m)


def format_time(timestamp):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))


def fileTime(file):
    return [
        format_time(os.path.getatime(file)),
        format_time(os.path.getmtime(file)),
        format_time(os.path.getctime(file)),
    ]

print(fileTime(music))
date = get_create_time(music)
a = eyed3.load(music)
tag:Tag=a.tag
tag.artist='sdfsdfsdf'
tag.title='2323sd33'
tag.save()
tt = date.timestamp()
# tt = 1660053121
print(date,tt)
os.utime(music, (tt, tt))
print(get_create_time(music))
print(fileTime(music))
