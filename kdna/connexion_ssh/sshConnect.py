
from fabric import Connection



class SSHClient:
    def __init__(self, name,ip) -> None:
        self.user = name
        self.serverIP= ip

    def getSSHparameter(self):
        return self.user + '@' +self.serverIP
    
    def connect(self):
        try:
            return Connection(self.getSSHParameter())
        except:
            print("An error as occured: "+"\n{0.stderr}")
            return None
        
    


# sshCLient = SSHConnect("dzada")