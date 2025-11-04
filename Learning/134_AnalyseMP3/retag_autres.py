# retag_l'humour-d'inter.py
# Update mp3 tags for L'humour d'Inter
#
# 2025-10-21    PV

import os
import shutil
from common_fs import get_folders, get_all_files, file_part, stem_part
import eyed3    # type: ignore
import ffmpeg   # type: ignore

source = r"C:\MusicOD2\Podcasts\RadioFrance"
source_processed = r"C:\MusicOD2\Podcasts\RadioFrance.Processed"
source_archives = r"C:\MusicOD2\Podcasts\RadioFrance.Archives"

folder_to_chronique = {
    "Bertrand Chameroy": "France Inter - Le billet de Bertrand Chameroy",
    "Charline Vanhoenacker": "France Inter - Charline explose les faits",
    "Daniel Morin": "France Inter - Le billet de Daniel Morin",
    "David Castello-Lopes": "France Inter - La question de David Castello-Lopes",
    "Lisa Delmoitiez": "France Inter - Lisa Delmoitiez n'aurait pas fait comme ça",
    "Tanguy Pastureau": "Tanguy Pastureau maltraite l'info",
    "Yann Marguet": "France Inter - La chronique de Yann Marguet",
}

def update_tags(file_full_path: str, artist: str, album: str, title: str, year: str, genre: str, comment: str) -> bool:
    audiofile = eyed3.load(file_full_path)
    if audiofile is None:
        print(f"ERROR: Can't load file {file_full_path}")
        return False

    if audiofile.tag is None:
        audiofile.initTag()

    audiofile.tag.artist = artist
    audiofile.tag.album = album
    audiofile.tag.title = title
    audiofile.tag.recording_date = eyed3.core.Date(int(year))   # type: ignore
    audiofile.tag.comments.set(comment)                         # type: ignore
    audiofile.tag.genre = genre                                 # type: ignore
    audiofile.tag.save(encoding='utf-8')                        # type: ignore
    return True

def convert_m4a_to_mp3_with_tags(input_file, output_file):
    """
    Converts .m4a to .mp3 at 192kbps stereo, PRESERVING tags.
    Uses ffmpeg-python, which has no C compilation issues.
    """
    if not os.path.exists(input_file):
        print(f"Error: Input file not found: {input_file}")
        return

    try:
        (
            ffmpeg
            .input(input_file)
            .output(
                output_file,
                audio_bitrate='192k',   # 192 kbps
                #                audio_channels=2,       # Stereo
                #                codec_audio='libmp3lame',
                map_metadata=0,         # Copy metadata from input file (0)
                id3v2_version=3         # Use ID3v2.3 tags for best compatibility
            )
            .run(capture_stdout=True, capture_stderr=True, overwrite_output=True)
        )

        print("Conversion to .mp3 successful")

    except ffmpeg.Error as e:
        print("Error during conversion:")
        # The error message from ffmpeg is in stderr
        print(e.stderr.decode('utf-8'))
    except FileNotFoundError:
        print("Error: 'ffmpeg' executable not found.")
        print("Please ensure ffmpeg is installed and in your system's PATH.")


def process_folder(folder):
    artist = file_part(folder)
    for filefp in list(get_all_files(folder)):
        if filefp.endswith(".mp3") or filefp.endswith(".m4a"):
            file = file_part(filefp)
            chronique = folder_to_chronique[artist]
            print(artist + ":", file)

            processed_filefp = os.path.join(source_processed, artist, file).replace('.m4a', '.mp3')
            os.makedirs(os.path.dirname(processed_filefp), exist_ok=True)
            if filefp.endswith(".mp3"):
                shutil.copyfile(filefp, processed_filefp)
            else:
                convert_m4a_to_mp3_with_tags(filefp, processed_filefp)

            year = file[:4]
            album = chronique + " " + year
            title = stem_part(file)
            comment = file[:10]
            genre = "Humour"

            if update_tags(processed_filefp, artist, album, title, year, genre, comment):
                archive_filefp = filefp.replace(source, source_archives)
                os.makedirs(os.path.dirname(archive_filefp), exist_ok=True)
                shutil.move(filefp, archive_filefp)
            else:
                os.remove(processed_filefp)


for folder in get_folders(source, True):
    if not "L'humour d'inter" in folder:
        print("\n------------------\n" + folder)
        process_folder(folder)
