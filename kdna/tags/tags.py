"""We will use connexion instance gathered by the module
    If the service is running the tags.conf file could change"""

import os
from fabric import Connection

def addTags(connexionInstance: Connection,project: str,newTag: str,fileToTag: str,verbose=False):
    """arguments: ssh instance / name of the project / name of the tags
    In the file tag.conf we must identify the tag [tags] to write tags at the end 
    of the file"""

    newTaggedBackup=newTag+", "+fileToTag+"\n"
    pathToConfTag="./kdna/"+project+"/tags.conf"

    #Récupération en local du fichier de config sur les tags
    getTagConf(pathToConfTag,connexionInstance)
    
    #Ouverture du fichier de conf en lecture
    try:
        with open('tags.conf',"r") as tagFile:
            tagLines=tagFile.readlines()
        tagLines.pop(0)
    except:
        raise Exception("Erreur de permission: read sur tags.conf")

    #Vérification que le tag n'est pas déjà utilisé
    for line in tagLines:
        tagFileCouple=line.split(", ")
        if(newTag == tagFileCouple[0]):
            os.remove('tags.conf')
            raise Exception(f"Le tag {tagFileCouple[0]} est déjà associé la backup {tagFileCouple[1]}")
        
    #Vérification que la sauvegarde existe sur le serveur
    try:
        if connexionInstance.run(f"find ./kdna/{project}/{fileToTag}"):
            pass
    except:
        raise Exception(f"Erreur: la sauvegarde {fileToTag} n'existe pas")

    #Ouverture du fichier de conf en append
    try:
        with open('tags.conf',"a") as tagFile:
            tagFile.write(newTaggedBackup)
    except:
        raise Exception(f"Erreur de permission: append sur tags.conf")
    
    #Renvoie du fichier sur le serveur
    try:
        connexionInstance.put("tags.conf",pathToConfTag)
    except:
        raise Exception("Erreur lors du renvoie du fichier sur le serveur")
    
    #Print+clean du fichier local
    if(verbose):
        print(f"Le fichier {fileToTag} est maintenant taggé par {newTag}")
    os.remove('tags.conf')



def deleteTags(connexionInstance: Connection,project: str,oldTag: str,verbose=False):
    """arguments: oldTag """

    #Validateur
    removed=False
    pathToConfTag="./kdna/"+project+"/tags.conf"
    #Récupération en local du fichier de config sur les tags
    getTagConf(pathToConfTag,connexionInstance)

    #Ouverture du fichier de conf en lecture
    try:
        with open('tags.conf',"r") as tagFile:
            tagLines=tagFile.readlines()
    except:
        raise Exception("Erreur de permission: read sur tags.conf")
    
    #Ouverture du fichier conf en écriture
    try:
        with open('tags.conf',"w") as tagFile:
            for line in tagLines:
                tag=line.split(", ")[0]
                if(tag!=oldTag):
                    tagFile.write(line)
                else:
                    file=line.split(", ")[1].strip('\n')
                    removed=True
    except:
        raise Exception("Erreur de permission: write sur tags.conf")
                
    if(not removed):
        os.remove('tags.conf')
        raise Exception(f"Aucun tag {oldTag} n'a été trouvé pour la supression")
    else:
        if(verbose):
            print(f"Le tag {oldTag} associé au fichier {file} a été supprimé")
    
    try:
        connexionInstance.put("tags.conf",pathToConfTag)
        os.remove('tags.conf')
    except:
        os.remove('tags.conf')
        raise Exception("La deletion de tag n'a pas été appliqué sur le server")

def updateTags(connexionInstance: Connection, project: str, oldTag: str, newTag: str, fileToTag: str,verbose=False):
    try:
        deleteTags(connexionInstance, project, oldTag)
    except:
        raise Exception("Une erreur est survenue lors de la tentative de suppression du tag")

    try:
        addTags(connexionInstance, project, newTag, fileToTag)
    except:
        raise Exception("Une erreur est survenue lors de la tentative de création du tag")
    if(verbose):
        print(f"Le tag {oldTag} a été modifié en {newTag}")
    
    

def readTags(connexionInstance: Connection,project: str):
    pathToConfTag="./kdna/"+project+"/tags.conf"

    #Récupération en local du fichier de config sur les tags
    getTagConf(pathToConfTag,connexionInstance)

    #Sélection des couples Tag, Fichier
    with open('tags.conf',"r") as tagFile:
        tagLines=tagFile.readlines()
    tagLines.pop(0)

    #Affichage des Tags dans la console
    print("Voici les tags de vos fichiers")
    for line in tagLines:
        tagFileCouple=line.split(", ")
        print('{:>8} {:>8}'.format(tagFileCouple[0],tagFileCouple[1]))
    os.remove('tags.conf')

def getFileNameByTag(connexionInstance: Connection,project: str,tag:str):
    pathToTag=f"/kdna/{project}/tags.conf"
    found = False
    #récupération du fichier tag.conf
    getTagConf(pathToTag,connexionInstance)
    #Recherche dans le fichier si un tag correspond a un fichier
    with open("tag.conf","r") as tagFile:
        for line in tag:
            tagFileCouple= line.split(", ")
            if(tagFileCouple[0]==tag):
                found=True
                os.remove('tags.conf')
                return tagFileCouple[1]
    #Si aucun fichier n'est trouvé une erreur apparait
    if(not found):
        raise Exception(f"Aucun fichier n'a été associé au tag {tag} dans le project {project}")
    

def getTagConf(pathToConfTag:str,connexionInstance: Connection):
    try:
        connexionInstance.get(pathToConfTag)
    except:
        raise Exception("Erreur lors de l'accès au fichier de configuration des tags")



readTags(Connection('test'),'projects')