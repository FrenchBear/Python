# retag_l'humour-d'inter.py
# Update mp3 tags for L'humour d'Inter
#
# 2025-10-21    PV
# 2025-11-05    PV      Force convert .mp3 to 192 kbps; Update cover images
# 2025-12-02    PV      MusicOD -> MusShared

# Notes:
# Images are not updated, need to do that later
#

import os
import shutil
import sys
from common_fs import get_folders, get_all_files, file_part, stem_part, extension_part
import eyed3    # type: ignore
import ffmpeg   # type: ignore

source = r"C:\MusShared\Podcasts\RadioFrance"
source_processed = r"C:\MusShared\Podcasts\RadioFrance.Processed"
source_archives = r"C:\MusShared\Podcasts\RadioFrance.Archives"

folder_to_chronique_cover: dict[str, tuple[str, str | None]] = {
    "Bertrand Chameroy": ("France Inter - Le billet de Bertrand Chameroy", r"C:\MusShared\Humour\Bertrand Chameroy\F1 - Le billet de\Le billet de Bertrand Chameroy.jpg"),
    "Charline Vanhoenacker": ("France Inter - Charline explose les faits", r"C:\MusShared\Humour\Charline Vanhoenacker\F1 - Charline explose les faits\Charline explose les faits.jpg"),
    "Daniel Morin": ("France Inter - Le billet de Daniel Morin", r"C:\MusShared\Humour\Daniel Morin\F1 - Le billet de\Le billet de Daniel Morin.jpg"),
    "David Castello-Lopes": ("France Inter - La question de David Castello-Lopes", r"C:\MusShared\Humour\David Castello-Lopes\F1 - La question de\La question de David Castello-Lopes.jpg"),
    "Lisa Delmoitiez": ("France Inter - Lisa Delmoitiez n'aurait pas fait comme ça", r"C:\MusShared\Humour\Lisa Delmoitiez\F1 - N'aurait pas fait comme ça\Lisa Delmoitiez n'aurait pas fait comme ça.jpg"),
    "Tanguy Pastureau": ("Tanguy Pastureau maltraite l'info", r"C:\MusShared\Humour\Tanguy Pastureau\Tanguy Pastureau maltraite l'info 2025.jpg"),
    "Yann Marguet": ("France Inter - La chronique de Yann Marguet", r"C:\MusShared\Humour\Yann Marguet\F1 - Moi, c'que j'en dis\La chronique de Yann Marguet.jpg"),
}

def memoize_image_data(f):
    memory = {}

    def inner(s):
        if s not in memory:
            memory[s] = f(s)
        return memory[s]

    return inner

@memoize_image_data
def get_image_data(cover_image_path: str) -> bytes | None:
    try:
        with open(cover_image_path, "rb") as f:
            image_data = f.read()
            return image_data
    except FileNotFoundError:
        print(f"ERROR: Cover art file not found at: {cover_image_path}")
    except Exception as e:
        print(f"ERROR: Could not read image file: {e}")
    return None


def update_tags_and_cover(file_full_path: str, artist: str, album: str, title: str, year: str, genre: str, comment: str, cover_mage_path: str | None) -> bool:
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
    audiofile.tag.copyright = ''                                # type: ignore
    audiofile.tag.encoded_by = ''                               # type: ignore

    # Replace image
    if cover_mage_path:
        image_data = get_image_data(cover_mage_path)
        if image_data:
            audiofile.tag.images.remove(u'')   # type: ignore
            ext = extension_part(cover_mage_path).casefold()
            match ext:
                case ".jpg":
                    mime_type = "image/jpeg"
                case ".png":
                    mime_type = "image/png"
                case _:
                    print("Unknown image suffix:", cover_mage_path)
                    print("*** Fatal error, abort")
                    sys.exit(1)
            audiofile.tag.images.set(3, image_data, mime_type, u"Cover")    # type: ignore

    audiofile.tag.save(encoding='utf-8')                        # type: ignore

    return True

def convert_to_mp3_192_with_tags(input_file, output_file) -> bool:
    """
    Converts .m4a to .mp3 at 192kbps stereo, PRESERVING tags.
    Uses ffmpeg-python, which has no C compilation issues.
    """
    if not os.path.exists(input_file):
        print(f"Error: Input file not found: {input_file}")
        return False

    try:
        (
            ffmpeg
            .input(input_file)
            .output(
                output_file,
                audio_bitrate='192k',   # 192 kbps
                map_metadata=0,         # Copy metadata from input file. Use -1 to strip all metadata
                id3v2_version=3         # Use ID3v2.3 tags for best compatibility
            )
            .run(capture_stdout=True, capture_stderr=True, overwrite_output=True)
        )

        print("Conversion to .mp3 successful")
        return True

    except ffmpeg.Error as e:
        print("Error during conversion:")
        # The error message from ffmpeg is in stderr
        print(e.stderr.decode('utf-8'))
    except FileNotFoundError:
        print("Error: 'ffmpeg' executable not found.")
        print("Please ensure ffmpeg is installed and in your system's PATH.")
    return False


def process_folder(folder):
    artist = file_part(folder)
    for filefp in list(get_all_files(folder)):
        if filefp.endswith(".mp3") or filefp.endswith(".m4a"):
            file = file_part(filefp)
            (chronique, cover) = folder_to_chronique_cover[artist]
            print(artist + ":", file)

            # # Convert all files including .mp3 to standardize output at 192 kbps
            processed_filefp = os.path.join(source_processed, artist, file).replace('.m4a', '.mp3')
            os.makedirs(os.path.dirname(processed_filefp), exist_ok=True)
            if not convert_to_mp3_192_with_tags(filefp, processed_filefp):
                print("*** Error during conversion to mp3 of", filefp)
                print("*** Aborting")
                sys.exit(1)

            year = file[:4]
            album = chronique + " " + year
            title = stem_part(file)
            comment = file[:10]
            genre = "Humour"

            if update_tags_and_cover(processed_filefp, artist, album, title, year, genre, comment, cover):
                archive_filefp = filefp.replace(source, source_archives)
                os.makedirs(os.path.dirname(archive_filefp), exist_ok=True)
                shutil.move(filefp, archive_filefp)
            else:
                os.remove(processed_filefp)


for folder in get_folders(source, True):
    if not "L'humour d'inter" in folder:
        print("\n------------------\n" + folder)
        process_folder(folder)
