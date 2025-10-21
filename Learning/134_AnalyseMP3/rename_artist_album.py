# rename_artist_album.py
# Update mp3 tags for L'humour d'Inter
#
# 2025-10-21    PV

from common_fs import get_all_files, file_part, stem_part
import eyed3
import os

source = r"C:\Temp\LP\L'humour d'Inter"

folder_to_artist = {
    r"La chronique de Merwane Benlazar": "Merwane Benlazar",
    r"La chronique de Rosa Bursztein": "Rosa Bursztein",
    r"La chronique de Tania Dutel": "Tania Dutel",
    r"La chronique de Thomas Croisière": "Thomas Croisière",
    r"La chronique de Tristan Lopin": "Tristan Lopin",
    r"La chronique de Yann Marguet": "Yann Marguet",
    r"La drôle d'humeur d'Amandine Lourdel": "Amandine Lourdel",
    r"La drôle d'humeur de Julie Conti": "Julie Conti",
    r"La drôle d'humeur de Julien Santini": "Julien Santini",
    r"La drôle d'humeur de Mélodie Fontaine": "Mélodie Fontaine",
    r"La drôle d'humeur de Rebecca Balestra": "Rebecca Balestra",
    r"La drôle d'humeur de Tom Baldetti": "Tom Baldetti",
    r"La drôle d'humeur d'Oldelaf": "Oldelaf",
    r"La question de David Castello-Lopes": "David Castello-Lopes",
    r"Le billet d'Alexandre Kominek": "Alexandre Kominek",
    r"Le billet de Bertrand Chameroy": "Bertrand Chameroy",
    r"Le billet de Daniel Morin": "Daniel Morin",
    r"Le billet de François Morel": "François Morel",
    r"Le billet de François Rollin": "François Rollin",
    r"Le billet de Jonathan Lambert": "Jonathan Lambert",
    r"Le billet de Lison Daniel": "Lison Daniel",
    r"Le billet de Marie s'Infiltre": "Marie s'Infiltre",
    r"Le billet de Matthieu Noël": "Matthieu Noël",
    r"Le billet de Sophia Aram": "Sophia Aram",
    r"Les nouvelles du monde d'Alexis le Rossignol": "Alexis le Rossignol",
    r"L'hommage d'Emma Bojan": "Emma Bojan",
    r"L'humour c'était mieux avant": "L'humour c'était mieux avant",
    r"Lisa Delmoitiez n'aurait pas fait comme ca": "Lisa Delmoitiez",
    r"Lisa Perrio moi ce que j'en dis": "Lisa Perrio",
    r"Lucie Carbone moi ce que j'en dis": "Lucie Carbone",
    r"Sofia Belabbes moi ce que j'en dis": "Sofia Belabbes",
    r"Tanguy Pastureau maltraite l'info": "Tanguy Pastureau",
    r"Bruno Peki n'aurait pas fait comme ca": "Bruno Peki",
    r"Charline explose les faits": "Charline Vanhoenacker",
    r"Emma Bojan n'a pas compris": "Emma Bojan",
    r"Fraîcheur marine": "Marine Baousson",
    r"La chronique de Ahmed Sparrow": "Ahmed Sparrow",
    r"La chronique de Benjamin Tranié": "Benjamin Tranié",
    r"La chronique de Camille Lavabre": "Camille Lavabre",
    r"La chronique de Camille Lorente": "Camille Lorente",
    r"La chronique de Charles Nouveau": "Charles Nouveau",
    r"La chronique de Guigui Pop": "Guigui Pop",
    r"La chronique de Harold Barbe": "Harold Barbe",
    r"La chronique de Jesse": "Jesse",
    r"La chronique de Karim Duval": "Karim Duval",
    r"La chronique de Laura Domenge": "Laura Domenge",
    r"La chronique de Lisa Perrio": "Lisa Perrio",
    r"La chronique de Lucie Carbone": "Lucie Carbone",
    r"La chronique de Mahaut Drama": "Mahaut Drama",
    r"La chronique de Marie de Brauer": "Marie de Brauer",
    r"La chronique de Marine Leonardi": "Marine Leonardi",
}

def update_tags(file_full_path: str, title: str, artist: str, year: str, comment: str):
    """Update mp3 tags of a file"""
    audiofile = eyed3.load(file_full_path)
    if audiofile is None:
        print(f"ERROR: Can't load file {file_full_path}")
        return

    if audiofile.tag is None:
        audiofile.initTag()

    audiofile.tag.artist = artist
    #audiofile.tag.album = "L'humour d'Inter"
    audiofile.tag.title = title
    audiofile.tag.recording_date = eyed3.core.Date(int(year))
    audiofile.tag.comments.set(comment)
    audiofile.tag.save(encoding='utf-8')

for filefp in list(get_all_files(source)):
    if filefp.endswith(".mp3"):
        parent = file_part(os.path.dirname(filefp))
        if parent in folder_to_artist:
            artist = folder_to_artist[parent]
        else:
            print("Artist not found:", filefp)
            breakpoint()

        file = file_part(filefp)
        title = stem_part(file)
        year = file[:4]
        comment = file[:10]

        print(file)
        # print("title:", title)
        # print("artist:", artist)
        # print("year:", year)
        # print("comment:", comment)
        # print()
        update_tags(filefp, title, artist, year, comment)