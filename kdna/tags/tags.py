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
    os.remove('tags.conf')

def deleteTags(connexionInstance,project,oldTag,newFile):
    """arguments: """
    return

def readTags():
    return

addTags(client,'project1','superTag','hey.zip')