from datetime import datetime
from eyed3.core import Tag


class Music():
    name: str       # only file name
    path: str       # full path
    dir: str        # dir
    date: datetime  # create time
    artist: str
    album: str
    title: str
    is_update: bool = False  # has been fixed
    is_good: bool = True
    tag: Tag
