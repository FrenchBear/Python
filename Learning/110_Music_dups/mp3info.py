# mp3info.py
# First experimennts retrieving mp3 tags
#
# 2022-06-07    PV

'''
Using eyeD3 library
https://eyed3.readthedocs.io/en/latest/


https://stackoverflow.com/questions/8948/accessing-mp3-metadata-with-python

'''

from cmath import pi
import eyed3
import eyed3.id3
import logging
import io
from common_fs import *


def check_tag(file: str):
    # https://stackoverflow.com/questions/36636063/python-eyed3-lame-tag-crc-check-failed
    # Redirect log from stdout to a sting (and ignore it!)
    log_stream = io.StringIO()
    logging.basicConfig(stream=log_stream, level=logging.INFO)

    af = eyed3.core.load(file, eyed3.id3.ID3_V2)
    artist:str = af.tag.artist
    album:str = af.tag.album
    title:str = af.tag.title.replace("’", "'").replace('?','¿')
    track:str = af.tag.track_num[0]

    # Just test if title starts with a without accent (it's Ok en English, probably not in French)
    # if title.lower().startswith('a '):
    #     print(file)
    # return

    file_basename = basename(filepart(file))

    # nn - Title
    if track:
        tag_basename = f'{track:0>2} - {title}'
        if file_basename == tag_basename:
            return
        tag_basename = f'{track:0>2} - {artist} - {title}'
        if file_basename == tag_basename:
            return
        tag_basename = f'{track:0>2} - {artist} - {album} - {title}'
        if file_basename == tag_basename:
            return
        tag_basename = f'{track:0>2} - {album} - {title}'
        if file_basename == tag_basename:
            return
        tag_basename = f'{artist} - {album} - {track:0>2} - {title}'        # Les charlots
        if file_basename == tag_basename:
            return

    # Artist - Title
    tag_basename = f'{artist} - {title}'
    if file_basename == tag_basename:
        return

    print('Tag diff for', file)
    print('Artist', artist)
    print('Album ', album)
    print('Title ', title)
    print('Track ', track)
    print()

#file = r"C:\Users\Pierr\OneDrive\MusicOD\A_Trier\A_Trier Préparé\Le grand Jojo\Le Grand JoJo - Ali Baba.mp3"
#check_tag(file)

root = r'C:\Users\Pierr\OneDrive\MusicOD\A_Trier\A_Trier Préparé\Dave'
root = r'C:\Users\Pierr\OneDrive\MusicOD\A_Trier\A_Trier Préparé\Michel Sardou - 1967-2010'
root = r'C:\Users\Pierr\OneDrive\MusicOD\A_Trier\A_Trier Préparé'
root = r'C:\Users\Pierr\OneDrive\MusicOD\A_Trier\Music Extra\Claude Bolling'
root = r'C:\Users\Pierr\OneDrive\MusicOD\MP3P\Chansons France'

n = 0
for file in get_all_files(root):
    if file.lower().endswith('.mp3'):
        n += 1
        check_tag(file)

print(n, 'file(s) checked.')
