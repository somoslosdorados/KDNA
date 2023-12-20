## POC-Parsing

Ce POC permet de récupérer un document au format .conf et de le parser afin de récupérer les caractéristiques des serveurs et des auto-backups qui y sont inscrites.
La lecture du fichier de configuration va faire appel à des stratégies différentes en fonction des headers ("[...]") lu et affecter les informations à des instances de classe.

Pour ce POC j'ai travaillé en grande majorité seule (85%), au début et à la fin du projet j'ai pu discuter avec Tristan et Giada pour trouver une bonne façon d'appliquer des stratégies différenciées.
