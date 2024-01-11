"""We will use connexion instance gathered by the module
    If the service is running the tags.conf file could change
    
    authors: Dorian TETU, Hugo PONTHIEU"""

import os
import time
from fabric import Connection
from kdna.connexion_ssh.sshConnect import SSHClient

def backup_exist(connection_instance: Connection,project: str,file_to_tag: str):
        # Vérification que la sauvegarde existe sur le serveur
    try:
        connection_instance.run(f"find ./kdna/{project}/{file_to_tag}",hide=True)
    except FileNotFoundError:
        raise FileNotFoundError(f"Erreur: la sauvegarde {file_to_tag} n'existe pas")

def add_tags(connection_instance: Connection, project: str, new_tag: str, file_to_tag: str, verbose=False):
    """arguments: ssh instance / name of the project / name of the tags
    In the file tag.conf we must identify the tag [tags] to write tags at the end 
    of the file
    
    authors: Dorian TETU, Hugo PONTHIEU"""

    new_tagged_backup = new_tag+", "+file_to_tag+"\n"
    path_to_conf_tag = "./kdna/"+project+"/tags.conf"
    #VERIFIER QUE LES TAGS NE SONT PAS EXISTANT !!!!!!!!!!!!!
    #Vérification que la backup existe sur le serveur
    backup_exist(connection_instance,project,file_to_tag)

    #Ecrire dans le fichier tag.conf le nouveau tag
    try:
        connection_instance.run(f"echo {new_tagged_backup} >> {path_to_conf_tag}")
    except PermissionError:
        raise PermissionError("Erreur de permission: read sur tags.conf")
    except ConnectionError:
        raise ConnectionError("Erreur de connexion lors de l'ajout d'un tag")


def delete_tags(connection_instance: Connection, project: str, oldTag: str, verbose=False):
    """arguments: oldTag """

    # Validateur
    removed = False
    path_to_conf_tag = "./kdna/"+project+"/tags.conf"

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
        connection_instance.put("tags.conf", path_to_conf_tag)
        os.remove('tags.conf')
    except:
        os.remove('tags.conf')
        raise PermissionError("La deletion de tag n'a pas été appliqué sur le server")


def update_tags(connection_instance: Connection, project: str, oldTag: str, new_tag: str, file_to_tag: str, verbose=False):
    try:
        delete_tags(connection_instance, project, oldTag)
    except:
        raise PermissionError("Une erreur est survenue lors de la tentative de suppression du tag")

    try:
        add_tags(connection_instance, project, new_tag, file_to_tag)
    except:
        raise PermissionError("Une erreur est survenue lors de la tentative de création du tag")
    if (verbose):
        print(f"Le tag {oldTag} a été modifié en {new_tag}")

def get_file_name_by_tag(connection_instance: Connection,project: str,tag:str) -> str:
    dico = get_tag_conf(connection_instance,project)
    if tag in dico:
        return dico[tag]
    # Si aucun fichier n'est trouvé une erreur apparait
    raise FileNotFoundError(f"Aucun fichier n'a été associé au tag {tag} dans le project {project}")
    
def check_init_tag_file(connection_instance: Connection, project: str):
    path_to_conf_tag = "./kdna/"+project+"/tags.conf"
    try:
        connection_instance.run(f"find {path_to_conf_tag}", hide=True)
    except PermissionError:
        raise PermissionError("Erreur de permission lors de l'acces à tags.conf")
    except:
        connection_instance.run(f"echo '[tags]' > {path_to_conf_tag}", hide=True)

def tag_exists(dico: dict, tag: str) -> bool:
    """Check if the tag exists in the project"""
    if tag in dico:
        return True
    return False


def generate_tag_name_(connection_instance: Connection, project: str, prefix: str) -> str:
    ct = time.time()
    new_tag = prefix + "_" + str(ct)
    new_tag_decorated = new_tag

    #check if the tag exists
    if tag_exists(get_tag_conf(connection_instance,project), new_tag):
        found = False
        while not found:
            #increment the tag, exemple: tag_1, tag_2, tag_3
            ct += 1
            new_tag_decorated = new_tag + "_" + ct
            if not tag_exists(get_tag_conf(connection_instance,project), new_tag_decorated):
                found = True
    return new_tag_decorated

def get_tag_conf(connection_instance: Connection, project: str) -> dict:
    """Get the tag.conf file and return a dictionnary with the tags, exemple: {"tag1": "file1", "tag2": "file2"}"""
    path_to_conf_tag = "./kdna/"+project+"/tags.conf"
    check_init_tag_file(connection_instance, project)
    result = connection_instance.run(f"cat {path_to_conf_tag}", hide=True)
    resultset = result.stdout.splitlines()
    resultset.pop(0)
    dictionnaire = {}
    for line in resultset:
        if line != "":
            dictionnaire[line.split(", ")[0]] = line.split(", ")[1]
    return dictionnaire

def write_tag_conf(connection_instance: Connection, project: str, dictionnaire: dict):
    """Write the dictionnary in the tag.conf file"""
    path_to_conf_tag = "./kdna/"+project+"/tags.conf"
    texte_conf = "[tags]\n"
    for key in dictionnaire:
        texte_conf += key + ", " + dictionnaire[key] + "\n"
    try:
        connection_instance.run(f"echo \"{texte_conf}\" > {path_to_conf_tag}", hide=True)
    except PermissionError:
        raise PermissionError("Erreur de permission: write sur tags.conf")

c = Connection("debian12.local")
dic = get_tag_conf(c,"project")
c.run("rm ./kdna/project/tags.conf")
write_tag_conf(c,"project",dic)