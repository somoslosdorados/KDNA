
from fabric import Connection
from kdna.logger.logger import log



class SSHClient:
    
    
    def __init__(self,name,ip) -> None:
        self.user = name
        self.serverIP= ip
        self.SSHInstance = None

    def getSSHparameter(self):
        return self.user + '@' +self.serverIP
    
    def connect(self):
        try:
            self.SSHInstance=Connection(self.getSSHParameter())
        except:
            print("An error as occured on connection")
            log("ERROR", "An error as occured on connection")
            return None
        
    def closeConnection(self):
        try:
            self.SSHInstance.close()
        except:
            print("An error as occured while closing ssh instance")
            log("ERROR", "An error as occured while closing ssh instance")
            return None
            
    def sendCommand(self,command):
        try:
            result = self.SSHInstance.run(command, hide=True)
            msg = "\n{0.stdout}"            
        except:
            print("An error as occured: "+ "\n{0.stderr}")
            log("ERROR", "An error as occured: "+ "\n{0.stderr}")
            return None
        


# sshCLient = SSHConnect("dzada")
