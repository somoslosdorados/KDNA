"""We will use connexion instance gathered by the module
    If the service is running the tags.conf file could change
    
    authors: Dorian TETU, Hugo PONTHIEU"""

import os
from fabric import Connection


def add_tags(connexion_instance: Connection, project: str, new_tag: str, file_to_tag: str, verbose=False):
    """arguments: ssh instance / name of the project / name of the tags
    In the file tag.conf we must identify the tag [tags] to write tags at the end 
    of the file
    
    authors: Dorian TETU, Hugo PONTHIEU"""

    new_tagged_backup = new_tag+", "+file_to_tag+"\n"
    path_to_conf_tag = "./kdna/"+project+"/tags.conf"

    # Récupération en local du fichier de config sur les tags
    get_tag_conf(path_to_conf_tag, connexion_instance)

    # Ouverture du fichier de conf en lecture
    try:
        with open('tags.conf', "r") as tag_file:
            tag_lines = tag_file.readlines()
        tag_lines.pop(0)
    except:
        raise PermissionError("Erreur de permission: read sur tags.conf")

    # Vérification que le tag n'est pas déjà utilisé
    for line in tag_lines:
        tag_file_couple = line.split(", ")
        if (new_tag == tag_file_couple[0]):
            os.remove('tags.conf')
            raise FileExistsError(f"Le tag {tag_file_couple[0]} est déjà associé la backup {tag_file_couple[1]}")

    # Vérification que la sauvegarde existe sur le serveur
    try:
        connexion_instance.run(f"find ./kdna/{project}/{file_to_tag}")
    except:
        raise FileNotFoundError(f"Erreur: la sauvegarde {file_to_tag} n'existe pas")

    # Ouverture du fichier de conf en append
    try:
        with open('tags.conf', "a") as tag_file:
            tag_file.write(new_tagged_backup)
    except:
        raise PermissionError("Erreur de permission: append sur tags.conf")

    # Renvoie du fichier sur le serveur
    try:
        connexion_instance.put("tags.conf", path_to_conf_tag)
    except:
        raise PermissionError("Erreur lors du renvoie du fichier sur le serveur")

    # Print+clean du fichier local
    if (verbose):
        print(f"Le fichier {file_to_tag} est maintenant taggé par {new_tag}")
    os.remove('tags.conf')


def delete_tags(connexion_instance: Connection, project: str, oldTag: str, verbose=False):
    """arguments: oldTag """

    # Validateur
    removed = False
    path_to_conf_tag = "./kdna/"+project+"/tags.conf"
    # Récupération en local du fichier de config sur les tags
    get_tag_conf(path_to_conf_tag, connexion_instance)

    # Ouverture du fichier de conf en lecture
    try:
        with open('tags.conf', "r") as tag_file:
            tag_lines = tag_file.readlines()
    except:
        raise PermissionError("Erreur de permission: read sur tags.conf")

    # Ouverture du fichier conf en écriture
    try:
        with open('tags.conf', "w") as tag_file:
            for line in tag_lines:
                tag = line.split(", ")[0]
                if (tag != oldTag):
                    tag_file.write(line)
                else:
                    file = line.split(", ")[1].strip('\n')
                    removed = True
    except:
        raise PermissionError("Erreur de permission: write sur tags.conf")

    if (not removed):
        os.remove('tags.conf')
        raise FileNotFoundError(f"Aucun tag {oldTag} n'a été trouvé pour la supression")
    else:
        if (verbose):
            print(f"Le tag {oldTag} associé au fichier {file} a été supprimé")

    try:
        connexion_instance.put("tags.conf", path_to_conf_tag)
        os.remove('tags.conf')
    except:
        os.remove('tags.conf')
        raise PermissionError("La deletion de tag n'a pas été appliqué sur le server")


def update_tags(connexion_instance: Connection, project: str, oldTag: str, new_tag: str, file_to_tag: str, verbose=False):
    try:
        delete_tags(connexion_instance, project, oldTag)
    except:
        raise PermissionError("Une erreur est survenue lors de la tentative de suppression du tag")

    try:
        add_tags(connexion_instance, project, new_tag, file_to_tag)
    except:
        raise PermissionError("Une erreur est survenue lors de la tentative de création du tag")
    if (verbose):
        print(f"Le tag {oldTag} a été modifié en {new_tag}")


def read_tags(connexion_instance: Connection, project: str):
    path_to_conf_tag = "./kdna/"+project+"/tags.conf"

    # Récupération en local du fichier de config sur les tags
    get_tag_conf(path_to_conf_tag, connexion_instance)

    # Sélection des couples Tag, Fichier
    with open('tags.conf', "r") as tag_file:
        tag_lines = tag_file.readlines()
    tag_lines.pop(0)

    # Affichage des Tags dans la console
    print("Voici les tags de vos fichiers")
    for line in tag_lines:
        tag_file_couple = line.split(", ")
        print('{:>8} {:>8}'.format(tag_file_couple[0], tag_file_couple[1]))
    os.remove('tags.conf')

def get_file_name_by_tag(connexion_instance: Connection,project: str,tag:str,verbose: True):
    path_to_tag=f"./kdna/{project}/tags.conf"
    found = False
    # récupération du fichier tag.conf
    get_tag_conf(path_to_tag, connexion_instance)
    # Recherche dans le fichier si un tag correspond a un fichier
    with open("tags.conf", "r") as tag_file:

        for line in tag_file:
            tag_file_couple = line.split(", ")
            if (tag_file_couple[0] == tag):
                found = True
                os.remove('tags.conf')
                return tag_file_couple[1]
    # Si aucun fichier n'est trouvé une erreur apparait
    if (not found):
        raise FileNotFoundError(f"Aucun fichier n'a été associé au tag {tag} dans le project {project}")


def get_tag_conf(path_to_conf_tag: str, connexion_instance: Connection):
    try:
        connexion_instance.get(path_to_conf_tag)
    except:
        raise FileNotFoundError("Erreur lors de l'accès au fichier de configuration des tags")
