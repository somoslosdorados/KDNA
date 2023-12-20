"""We will use connexion instance gathered by the module
    If the service is running the tags.conf file could change"""
from fabric import Connection
import os

client = Connection('test@192.168.122.226')
def addTags(connexionInstance,project,newTag,newFile):
    """arguments: ssh instance / name of the project / name of the tags
    In the file tag.conf we must identify the tag [tags] to write tags at the end 
    of the file"""
    newTaggedBackup=newTag+", "+newFile+"\n"
    pathToConfTag="./kdna/"+project+"/tags.conf"
    connexionInstance.get(pathToConfTag)
    with open('tags.conf',"a") as tagFile:
        tagFile.write(newTaggedBackup)
    connexionInstance.put("tags.conf",pathToConfTag)
    print(f"Le fichier {newFile} est maintenant taggé par {newTag}")
    os.remove('tags.conf')

def deleteTags(connexionInstance,project,oldTag):
    """arguments: oldTag """
    removed=True
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
                removed=False
                break
    if(removed):
        print(f"Aucun tag {oldTag} n'a été trouvé pour la supression")
    else:
        print(f"Le tag {oldTag} associé au fichier {file} a été supprimé")
    connexionInstance.put("tags.conf",pathToConfTag)
    os.remove('tags.conf')
    return

def readTags(connexionInstance,project):
    pathToConfTag="./kdna/"+project+"/tags.conf"
    connexionInstance.get(pathToConfTag)
    with open('tags.conf',"r") as tagFile:
        tagLines=tagFile.readlines()
    for line in tagLines:
        tagFileCouple=line.split(", ")
        
    
    return

deleteTags(client,'project1','a')