"""We will use connexion instance gathered by the module"""
from fabric import Connection
import fabric

client = Connection('test@192.168.122.226')
def addTags(connexionInstance,path,tag):
    """argument: ssh instance / path to the tags.conf / name of the tags
    In the file tag.conf we must identify the tag [tags] to write tags at the end 
    of the file"""
    
    newTaggedBackup=tag+", "+path.split("/")[-1]
    print(newTaggedBackup)
    

def deleteTags():
    return

def readTags():
    return

addTags(client,'/kdna/project1/tag.conf','superTag')