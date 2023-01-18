import re

from src.type import Music


def fix_artist(artist: str):
    artist = artist.strip()
    artist = re.sub(r"^【|】$", "", artist)
    return artist

def fix_music(music: Music):
    try:
        arr = music.name.split("-")
        if len(arr) == 2:
            pre_artist = fix_artist(arr[0])
            pre_title = arr[1].strip()

            music.tag.artist = music.artist = pre_artist
            music.tag.title = music.title = pre_title

            music.is_update = True
    except:
        print("error", music.path)
        import traceback
        traceback.print_exc()
