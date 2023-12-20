## Parser

Ce POC permet de récupérer un document au format .conf et de le parser afin de récupérer les caractéristiques des serveurs et des auto-backups qui y sont inscrites.
La lecture du fichier de configuration va faire appel à des stratégies différentes en fonction des headers ("[...]") lus et affecter les informations à des instances de classe.
Les objets Serveur sont stockés dans la liste listServers.
Les objets AutoBackup sont stockés dans la liste listAutoBackups.