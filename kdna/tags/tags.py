"""We will use connexion instance gathered by the module
    If the service is running the tags.conf file could change"""

import os


def addTags(connexionInstance,project,newTag,fileToTag):
    """arguments: ssh instance / name of the project / name of the tags
    In the file tag.conf we must identify the tag [tags] to write tags at the end 
    of the file"""
    newTaggedBackup=newTag+", "+fileToTag+"\n"
    pathToConfTag="./kdna/"+project+"/tags.conf"
    connexionInstance.get(pathToConfTag)
    
    with open('tags.conf',"r") as tagFile:
        tagLines=tagFile.readlines()
    tagLines.pop(0)

    for line in tagLines:
        tagFileCouple=line.split(", ")
        if(newTag == tagFileCouple[0]):
            os.remove('tags.conf')
            raise Exception(f"Le tag {tagFileCouple[0]} est déjà associé la backup {tagFileCouple[1]}")

    with open('tags.conf',"a") as tagFile:
        tagFile.write(newTaggedBackup)
    connexionInstance.put("tags.conf",pathToConfTag)
    print(f"Le fichier {fileToTag} est maintenant taggé par {newTag}")
    os.remove('tags.conf')

def deleteTags(connexionInstance,project,oldTag):
    """arguments: oldTag """
    removed=False
    pathToConfTag="./kdna/"+project+"/tags.conf"
    connexionInstance.get(pathToConfTag)
    with open('tags.conf',"r") as tagFile:
        tagLines=tagFile.readlines()
    with open('tags.conf',"w") as tagFile:
        for line in tagLines:
            tag=line.split(", ")[0]
            if(tag!=oldTag):
                tagFile.write(line)
            else:
                file=line.split(", ")[1].strip('\n')
                removed=True
                
    if(not removed):
        os.remove('tags.conf')
        raise Exception(f"Aucun tag {oldTag} n'a été trouvé pour la supression")
    else:
        print(f"Le tag {oldTag} associé au fichier {file} a été supprimé")
    connexionInstance.put("tags.conf",pathToConfTag)
    os.remove('tags.conf')

def updateTags(connexionInstance, project, oldTag, newTag, fileToTag):
    try:
        deleteTags(connexionInstance, project, oldTag)
    except:
        raise Exception("Une erreur est survenue lors de la tentative de suppression du tag")

    try:
        addTags(connexionInstance, project, newTag, fileToTag)
    except:
        raise Exception("Une erreur est survenue lors de la tentative de création du tag")
    
    print(f"Le tag {oldTag} a été modifié en {newTag}")
    
    

def readTags(connexionInstance,project):
    pathToConfTag="./kdna/"+project+"/tags.conf"
    connexionInstance.get(pathToConfTag)
    with open('tags.conf',"r") as tagFile:
        tagLines=tagFile.readlines()
    tagLines.pop(0)
    print("Voici les tags de vos fichiers")
    for line in tagLines:
        tagFileCouple=line.split(", ")
        print('{:>8} {:>8}'.format(tagFileCouple[0],tagFileCouple[1]))
    os.remove('tags.conf')