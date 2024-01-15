# Documentation de l'API tags.py

Ce fichier README fournit des instructions sur la façon d'utiliser l'API tags.py pour gérer les tags dans votre application.

## Installation

Pour utiliser l'API tags.py, vous devez d'abord l'importer:
> from kdna.tags import tags

## Utilisation

### Créer un tag

Pour créer un tag, vous devez utiliser la fonction add_tags() de l'API tags.py. Cette fonction prend en paramètre :
- une instance de connexion fabric (obtenable avec le module ssh.ssh_client)
- le nom du projet
- le nom du tag
- le nom de la backup à tagger

> tags.add_tags(ssh_client.connection, project_name, tag_name, backup_name)

### Supprimer un tag

Pour supprimer un tag, vous devez utiliser la fonction delete_tags() de l'API tags.py. Cette fonction prend en paramètre :
- une instance de connexion fabric (obtenable avec le module ssh.ssh_client)
- le nom du projet
- le nom du tag

> tags.delete_tags(ssh_client.connection, project_name, tag_name)

### Modifier un tag

Pour modifier un tag, vous devez utiliser la fonction update_tags() de l'API tags.py. Cette fonction prend en paramètre :
- une instance de connexion fabric (obtenable avec le module ssh.ssh_client)
- le nom du projet
- le nom du tag
- le nouveau nom du tag

> tags.update_tags(ssh_client.connection, project_name, tag_name, new_tag_name)

### Recupérer les tags (dictionnaire python)

Pour récupérer les tags, vous devez utiliser la fonction get_tag_conf() de l'API tags.py. Cette fonction prend en paramètre :
- une instance de connexion fabric (obtenable avec le module ssh.ssh_client)
- le nom du projet

> tags.get_tag_conf(ssh_client.connection, project_name)
>> exemple de retour : {'tag1': 'backup1', 'tag2': 'backup2'}

### Générer un nom de tag unique (utile pour le cron)

Pour générer un nom de tag unique, vous devez utiliser la fonction generate_tag_name() de l'API tags.py. Cette fonction prend en paramètre :
- Une instance de connexion fabric (obtenable avec le module ssh.ssh_client)
- le nom du projet
- un préfixe 

> tags.generate_tag_name(ssh_client.connection, project_name, prefix)

### Savoir si un tag existe

Pour savoir si un tag existe, vous devez utiliser la fonction tag_exists() de l'API tags.py. Cette fonction prend en paramètre :
- Une instance de connexion fabric (obtenable avec le module ssh.ssh_client)
- le nom du projet
- le nom du tag

> tags.tag_exists(ssh_client.connection, project_name, tag_name)
>> retourne True si le tag existe, False sinon

