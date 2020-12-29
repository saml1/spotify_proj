import os
from mutagen.easyid3 import EasyID3
import mutagen.id3
import tracklist
from track import Track
from mutagen.mp3 import MP3


def create_tracklist_from_local_dr(directory):
    tp = tracklist.Tracklist()
    for subdir, dirs, files in os.walk(directory):
        for filename in files:
            filepath = subdir + os.sep + filename
            if filepath.endswith('.mp3'):
                try:
                    audio = EasyID3(filepath)
                    # print(audio)
                    audio_info = MP3(filepath).info
                    track = Track(audio['title'][0], audio['album'][0], audio['artist'][0], int(audio_info.length*1000))
                    # tp.add(Track(audio['title'], audio['album'], audio['artist'], int(audio_info.length*1000)))
                    tp.add(track)
                except mutagen.id3.ID3NoHeaderError:
                    print("\nthe following file doesn't start with an ID3 tag and cannot be read:\n" + filepath)
                except KeyError:
                    track = Track(audio['title'][0], None, audio['artist'][0], int(audio_info.length * 1000))
                    tp.add(track)
    return tp
