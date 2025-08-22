# wtj.py
# Conversions Wepb to Jpeg
#
# 2025-08-10    PV

import tempfile
import os
import subprocess
import shutil
from common_fs import file_exists, get_files

source = r"D:\Kaforas\OneDrive\PicturesODKB\!ToPost\To post X\Tumblr\Wepb"

def webp_to_jpeg(source):
    if not file_exists(source):
        print("Can't find file", source)
        return
    
    dest = source.casefold().replace(".webp", ".gif")

    tdir = tempfile.mkdtemp()
    os.chdir(tdir)
    lastframe = 0

    try:
        for i in range(1, 101):
            output_bytes = subprocess.check_output(['webpmux', '-get', 'frame', str(i), source, '-o', f'frame{i:03}.webp'])
            # output_string = output_bytes.decode('utf-8')
            # print(output_string)
            lastframe = i
    except:
        pass

    print("Last frame:", lastframe)

    subprocess.run(["ffmpeg", "-i", "frame%3d.webp", "-filter_complex", "[0:v] palettegen=reserve_transparent=1 [p];[0:v][p] paletteuse", dest])
    try:
        shutil.rmtree(tdir)
    except:
        pass


for file in get_files(source):
    if file.casefold().endswith(".webp"):
        webp_to_jpeg(os.path.join(source, file))
