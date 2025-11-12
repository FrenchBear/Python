# retag_l_humour_d_inter.py
# Update mp3 tags for L'humour d'Inter
#
# 2025-10-21    PV

import os
import shutil
import sys
from common_fs import get_all_files, file_part, stem_part
import eyed3    # type: ignore
import ffmpeg   # type: ignore

source = r"C:\MusicOD2\Podcasts\RadioFrance\L'humour d'inter"
source_processed = r"C:\MusicOD2\Podcasts\RadioFrance.Processed\L'humour d'inter"
source_archives = r"C:\MusicOD2\Podcasts\RadioFrance.Archives\L'humour d'inter"

folder_to_artist_crhonique = {
    "la-chronique-de-merwane-benlazar": ("Merwane Benlazar", "La chronique de Merwane Benlazar"),
    "?? Rosa Bursztein": ("Rosa Bursztein", "La chronique de Rosa Bursztein"),
    "?? Tania Dutel": ("Tania Dutel", "La chronique de Tania Dutel"),
    "?? Thomas Croisière": ("Thomas Croisière", "La chronique de Thomas Croisière"),
    "la-chronique-de-tristan-lopin": ("Tristan Lopin", "La chronique de Tristan Lopin"),
    "la-chronique-de-yann-marguet": ("Yann Marguet", "La chronique de Yann Marguet"),
    "la-drole-d-humeur-d-amandine-lourdel-n-a-pas-compris": ("Amandine Lourdel", "La drôle d'humeur d'Amandine Lourdel"),
    "?? Julie Conti": ("Julie Conti", "La drôle d'humeur de Julie Conti"),
    "la-drole-d-humeur-de-julien-santini": ("Julien Santini", "La drôle d'humeur de Julien Santini"),
    "la-drole-d-humeur-de-melodie-fontaine": ("Mélodie Fontaine", "La drôle d'humeur de Mélodie Fontaine"),
    "?? Rebecca Balestra": ("Rebecca Balestra", "La drôle d'humeur de Rebecca Balestra"),
    "la-drole-d-humeur-de-tom-baldetti": ("Tom Baldetti", "La drôle d'humeur de Tom Baldetti"),
    "la-drole-d-humeur-d-oldelaf": ("Oldelaf", "La drôle d'humeur d'Oldelaf"),
    "la-question-de-david-castello-lopes": ("David Castello-Lopes", "La question de David Castello-Lopes"),
    "?? Alexandre Kominek": ("Alexandre Kominek", "Le billet d'Alexandre Kominek"),
    "le-billet-de-bertrand-chameroy": ("Bertrand Chameroy", "Le billet de Bertrand Chameroy"),
    "le-billet-de-daniel-morin": ("Daniel Morin", "Le billet de Daniel Morin"),
    "le-billet-de-francois-morel": ("François Morel", "Le billet de François Morel"),
    "le-billet-de-francois-rollin": ("François Rollin", "Le billet de François Rollin"),
    "?? Jonathan Lambert": ("Jonathan Lambert", "Le billet de Jonathan Lambert"),
    "?? Lison Daniel": ("Lison Daniel", "Le billet de Lison Daniel"),
    "?? Marie s'Infiltre": ("Marie s'Infiltre", "Le billet de Marie s'Infiltre"),
    "?? Matthieu Noël": ("Matthieu Noël", "Le billet de Matthieu Noël"),
    "le-billet-de-sophia-aram": ("Sophia Aram", "Le billet de Sophia Aram"),
    "les-nouvelles-du-monde": ("Alexis le Rossignol", "Les nouvelles du monde d'Alexis le Rossignol"),
    "l-hommage-d-emma-bojan": ("Emma Bojan", "L'hommage d'Emma Bojan"),
    "?? L'humour c'était mieux avant": ("L'humour c'était mieux avant", "L'humour c'était mieux avant"),
    "lisa-delmoitiez-n-aurait-pas-fait-comme-ca": ("Lisa Delmoitiez", "Lisa Delmoitiez n'aurait pas fait comme ca"),
    "la-chronique-de-sofia-belabbes": ("Sofia Belabbes", "Sofia Belabbes moi ce que j'en dis"),
    "tanguy-pastureau-maltraite-l-info": ("Tanguy Pastureau", "Tanguy Pastureau maltraite l'info"),
    "bruno-peki-n-aurait-pas-fait-comme-ca": ("Bruno Peki", "Bruno Peki n'aurait pas fait comme ca"),
    "charline-explose-les-faits": ("Charline Vanhoenacker", "Charline explose les faits"),
    "?? Emma Bojan": ("Emma Bojan", "Emma Bojan n'a pas compris"),
    "fraicheur-marine": ("Marine Baousson", "Fraîcheur marine"),
    "la-chronique-de-ahmed-sparrow": ("Ahmed Sparrow", "La chronique de Ahmed Sparrow"),
    "?? Benjamin Tranié": ("Benjamin Tranié", "La chronique de Benjamin Tranié"),
    "la-chronique-de-camille-lavabre": ("Camille Lavabre", "La chronique de Camille Lavabre"),
    "la-chronique-de-camille-lorente": ("Camille Lorente", "La chronique de Camille Lorente"),
    "?? Charles Nouveau": ("Charles Nouveau", "La chronique de Charles Nouveau"),
    "la-chronique-de-guigui-pop": ("Guigui Pop", "La chronique de Guigui Pop"),
    "la-chronique-de-harold-barbe": ("Harold Barbé", "La chronique de Harold Barbé"),
    "la-chronique-de-jesse": ("Jesse", "La chronique de Jesse"),
    "?? Karim Duval": ("Karim Duval", "La chronique de Karim Duval"),
    "?? Laura Domenge": ("Laura Domenge", "La chronique de Laura Domenge"),
    "la-chronique-de-lisa-perrio": ("Lisa Perrio", "La chronique de Lisa Perrio"),
    "?? Lucie Carbone 1": ("Lucie Carbone", "Lucie Carbone moi ce que j'en dis"),
    "?? Lucie Carbone 2": ("Lucie Carbone", "La chronique de Lucie Carbone"),
    "la-chronique-de-mahaut-drama": ("Mahaut Drama", "La chronique de Mahaut Drama"),
    "la-chronique-de-marie-de-brauer": ("Marie de Brauer", "La chronique de Marie de Brauer"),
    "la-chronique-de-marine-leonardi": ("Marine Leonardi", "La chronique de Marine Leonardi"),
    "vero-la-conciliatrice": ("Véro Clederman-Pilouchet", "Merci Véro"),
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
    audiofile.tag.copyright = ''                                # type: ignore
    audiofile.tag.encoded_by = ''                               # type: ignore
    audiofile.tag.save(encoding='utf-8')                        # type: ignore

    # For now, don't update cver images, but should probably standardize later

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


# First check for missing mappings
problem = False
for filefp in list(get_all_files(source)):
    if filefp.endswith(".mp3") or filefp.endswith(".m4a"):
        parent = file_part(os.path.dirname(filefp))
        if parent not in folder_to_artist_crhonique:
            print("Folder not found: ", parent)
            problem = True
if problem:
    sys.exit(0)


for filefp in list(get_all_files(source)):
    if filefp.endswith(".mp3") or filefp.endswith(".m4a"):
        parent = file_part(os.path.dirname(filefp))
        file = file_part(filefp)
        artist, correct_folder = folder_to_artist_crhonique[parent]
        print(artist + ":", file)

        # Convert all files including .mp3 to standardize output at 192 kbps
        processed_filefp = os.path.join(source_processed, correct_folder, file).replace('.m4a', '.mp3')
        os.makedirs(os.path.dirname(processed_filefp), exist_ok=True)
        if not convert_to_mp3_192_with_tags(filefp, processed_filefp):
            print("*** Error during conversion to mp3 of", filefp)
            print("*** Aborting")
            sys.exit(1)

        album = "L'humour d'inter"
        title = stem_part(file)
        year = file[:4]
        comment = file[:10]
        genre = "Humour"

        if update_tags(processed_filefp, artist, album, title, year, genre, comment):
            archive_filefp = filefp.replace(source, source_archives)
            os.makedirs(os.path.dirname(archive_filefp), exist_ok=True)
            shutil.move(filefp, archive_filefp)
        else:
            os.remove(processed_filefp)
