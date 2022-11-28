import os.path
import time
import os
import eyed3
music = "test.mp3"


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

get_info(music)
