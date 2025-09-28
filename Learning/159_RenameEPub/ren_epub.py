# ren_epub.py
#
# 2025-09-26    PV      Code written by Gemini

# Je voudrais un programme Python pour renommer les fichiers d'un dossier qui contient des fichiers .epub avec un titre
# en français à modifier.
# Le problème est la position des préfixes "Le", "La", "Les", "Une", "L'" qui sont placés à la fin du titre après une
# virgule et suivis d'un espace, qu'il faut déplacer en début de fichier.
#
# Par exemple, le fichier
# "droit de vote des femmes en France_ Un événement clé passé sousents t. 32, Le - 50minutes, & Spinassou, Rémi.epub"
# doit être renommé
# "Le droit de vote des femmes en France_ Un événement clé passé sousents t. 32 - 50minutes, & Spinassou, Rémi.epub"
# en supprimant ", Le" et en insérant "Le" en tête.

import os

do_it = True

def renommer_fichiers_epub():
    """
    Script pour renommer des fichiers .epub en déplaçant les articles 
    ("Le", "La", "Les", "Un", "Une", "L'") de la fin vers le début du nom.
    
    Exemple:
    "Titre du livre, Le - Auteur.epub" 
    devient 
    "Le Titre du livre - Auteur.epub"
    """
    # Demande à l'utilisateur de saisir le chemin du dossier
    #chemin_dossier = input("Veuillez glisser ou coller le chemin du dossier contenant les fichiers .epub, puis appuyez sur Entrée : ").strip()
    #chemin_dossier = r"W:\eBooks\Grands Événements"
    chemin_dossier = r"W:\eBooks\!Histoire 1929 livres\France\Histoire - Premier Empire"

    if not os.path.isdir(chemin_dossier):
        print(f"Erreur : Le dossier '{chemin_dossier}' n'existe pas ou est invalide.")
        return

    # Liste des articles à rechercher (avec une apostrophe pour "L'")
    articles_a_deplacer = ["Le", "La", "Les", "Un", "Une", "L'"]
    fichiers_renommes = 0
    fichiers_epub_trouves = 0

    print("\n--- Début du traitement ---")

    # Parcourir tous les fichiers dans le dossier spécifié
    for nom_fichier in os.listdir(chemin_dossier):
        
        # Ne traiter que les fichiers .epub
        if nom_fichier.lower().endswith('.epub'):
            fichiers_epub_trouves += 1
            nom_original_complet = os.path.join(chemin_dossier, nom_fichier)
            nom_sans_extension, extension = os.path.splitext(nom_fichier)
            
            # Itérer sur chaque article possible
            for article in articles_a_deplacer:
                # Créer le séparateur à rechercher, ex: ", Le" ou ", L'"
                separateur = f", {article} - "
                
                # Vérifier si le séparateur se trouve bien à la fin de la partie titre
                if separateur in nom_sans_extension:
                    
                    # On utilise rsplit pour s'assurer de ne traiter que la dernière occurrence
                    # C'est plus robuste si le titre contenait déjà ", Le"
                    parties = nom_sans_extension.rsplit(separateur, 1)
                    
                    if len(parties) == 2:
                        titre_principal = parties[0]
                        reste_du_nom = parties[1]
                        
                        # Recomposer le nouveau nom de fichier
                        if article=="L'":
                            nouveau_nom_sans_extension = f"{article}{titre_principal} - {reste_du_nom}"
                        else:
                            nouveau_nom_sans_extension = f"{article} {titre_principal} - {reste_du_nom}"
                        nouveau_nom_complet = os.path.join(chemin_dossier, nouveau_nom_sans_extension + extension)
                        
                        try:
                            if do_it:
                                os.rename(nom_original_complet, nouveau_nom_complet)
                            print(f'✅ Renommé : "{nom_fichier}"\n      -> "{nouveau_nom_sans_extension + extension}"')
                            fichiers_renommes += 1
                            # Sortir de la boucle des articles car le fichier a été renommé
                            break 
                        except OSError as e:
                            print(f"❌ Erreur lors du renommage de {nom_fichier} : {e}")

    print("\n--- Traitement terminé ---")
    print(f"Fichiers .epub trouvés : {fichiers_epub_trouves}")
    print(f"Fichiers renommés avec succès : {fichiers_renommes}")

# Lancer la fonction principale
if __name__ == "__main__":
    renommer_fichiers_epub()