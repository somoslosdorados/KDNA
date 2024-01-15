# KDNA

This is the official repository for the DO2023-2026 python CLI backup project

Après avoir cloné le dépôt, vous devrez installer toutes les dépendances

## Documentation - CRUD fichier de config

Pour créer le fichier de configuration faites la commande suivant :

```bash
Utils.initialize_config_file()
```

Un fichier est créé :

```
[server]
[auto-backup]
```

Vous pouvez désormais faire vos commandes dans le fichier `__main__.py`

### Server

Avant toute chose, pensez à instancier le service de serveur comme ceci dans le `__main__.py` : 

```
serviceServer = ServerService()
```

1. #### Création

Vous pouvez créer un serveur avec ces différents paramètres :

| Signature : | id_server | address | credentials |  port  |  alias |
| :---------- | :-------: | :-----: | :---------: | :----: | -----: |
| Type :      |  String   | String  |   String    | String | String |

Comme ceci :

```
serverService.create_server("S4", "dgrasset@32.432.43.56", "/path/ssh", "5432", "hello")
```

2. #### Suppression

Vous pouvez supprimer un serveur avec ces différents paramètres :

| Signature : |  id_server  |   by_alias |
| :---------- | :---------: | ---------: |
| Type :      |   String    |    Boolean |
| Règle :     | Obligatoire | Facultatif |

Vous pouvez supprimer un serveur grâce à son id de cette manière :

```
serverService.delete_server("18")
```

Mais vous pouvez aussi supprimer un serveur grâce à son alias de cette manière :

```
serverService.delete_server("hello", by_alias=True)
```

À noter que l'attribut `by_alias` possède de base la valeur `False` c'est pourquoi vous n'avez pas besoin de le préciser lorsque vous voulez effectuer une suppresion par id.

3. #### Mise à jour

Vous pouvez mettre à jour un serveur grâce à son alias avec ces différents paramètres :

| Signature : |    alias    | address    | credentials |    port    | nouvel alias |
| :---------- | :---------: | :--------: | :---------: | :--------: | -----------: |
| Type :      |   String    | String     | String      |   String   |       String |
| Règle :     | Obligatoire | Facultatif | Facultatif  | Facultatif |   Facultatif |

```
serverService.update_server("S4", new_port="25", new_address="bplanche@10.0.432.43", new_credentials=".ssh/path", new_alias="SS4")
```

À noter que vous n'êtes pas obligé de modifier tous les champs de votre ligne concernant le serveur que vous voulez modifier. Vous pouvez par exemple seulement changer le port en précisant `new_port` en plus de l'`alias` obligatoire dans la signature de votre update.

De plus l'id du serveur n'est pas modifiable, il sera peut être généré automatiquement plus tard.

4. #### Read

| Signature : |  alias_server  | 
| :---------- | -------------: |
| Type :      |   String       |
| Règle :     | Obligatoire    |


Si vous souhaitez afficher un serveur grace à son alias vous pouvez utiliser la commande suivante :

```
serverService.find_by_alias("SS4")
```

### Auto-Backup

Avant toute chose, pensez à instancier le service de serveur comme ceci dans le `__main__.py` : 

```
autoBackupService = AutoBackupService()
```

1. #### Création

Vous pouvez créer une auto-backup avec ces différents paramètres :

| Signature : | id_backup | frequency |  name  | timestamp | id_server |   path |
| :---------- | :-------: | :-------: | :----: | :-------: | :-------: | -----: |
| Type :      |  String   |  String   | String |  String   |  String   | String |

Comme ceci :

```
autoBackupService.create_auto_backup("9", "monthly", "okay", "2021-01-01", "3", "/home/backup")
```

2. #### Suppression

Vous pouvez supprimer une auto-backup grâce à son id de cette manière :

```
autoBackupService.delete_auto_backup("9")
```

3. #### Mise à jour

Vous pouvez mettre à jour une auto-backup grâce à son id avec ces différents paramètres :

| Signature : |  id_backup  | frequency  |    name    | timestamp  |       path |
| :---------- | :---------: | :--------: | :--------: | :--------: | ---------: |
| Type :      |   String    |   String   |   String   |   String   |     String |
| Règle :     | Obligatoire | Facultatif | Facultatif | Facultatif | Facultatif |

```
autoBackupService.update_auto_backup("9", new_frequency="daily", new_timestamp="2021-01-02", new_path="/home/backup")
```

À noter que vous n'êtes pas obligé de modifier tous les champs de votre ligne concernant l'auto-backup que vous voulez modifier. Vous pouvez par exemple seulement changer le nom en précisant `new_name` en plus de l'`id` obligatoire dans la signature de votre update.

De plus l'id relié au serveur n'est pas modifiable, car la back-up est lié à celui-ci

4. #### Read

| Signature : |  id_backup  | 
| :---------- | ----------: |
| Type :      |   String    |
| Règle :     | Obligatoire |


Si vous souhaitez afficher une auto-backup grace à son id vous pouvez utiliser la commande suivante :

```
autoBackupService.find_by_id("9")
```

### Lire tout la partie Auto-Backup & Server

Il est possible d'afficher tous les serveurs ou d'afficher toutes les auto-backups de notre fichier de configuration. Pour cela utiliser la commande suivante :
```
autoBackupService.find_all()
ou
serverService.find_all()
```