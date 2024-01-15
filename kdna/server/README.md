# KDNA

This is the official repository for the DO2023-2026 python CLI backup project.

After cloning the repository you need to install all dependencies.

## Documentation - CRUD of config file

Creation of the config file :

```bash
Utils.initialize_config_file()
```

A file is created : 

```
[server]
[auto-backup]
```
You can now call commands in the file `__main__.py`

### Server

Before anything, you need to instanciate the server service in the `__main__.py` : 

```
serviceServer = ServerService()
```

1. #### Creation

You can create a server with these parameters :

- id: server ID    (String)
- address: username@server address  (String)
- path: path to the SSH key     (String)
- port: port address    (String)
- alias: server tag     (String)
- encrypted: boolean indicating whether the backups for this server are encrypted   (Boolean)

Like this :

```
serverService.create_server("S4", "dgrasset@32.432.43.56", "/path/ssh", "5432", "hello", True)
```

2. #### Delete

You can delete a server with these parameters :

- id_server : server ID (String)   (mandatory)
- by_alias : alias of the server (Boolean)  (optional)

You can delete a server with the id like this :

```
serverService.delete_server("18")
```

You can also delete a server using its alias :

```
serverService.delete_server("hello", by_alias=True)
```

Note that the `by_alias` attribute has a default value of `False`, so you don't need to specify it when deleting by id.

3. #### Updating

You can update a server through its alias with these different parameters:

| Signature : |    alias    | address    | credentials |    port    | nouvel alias |
| :---------- | :---------: | :--------: | :---------: | :--------: | -----------: |
| Type :      |   String    | String     | String      |   String   |       String |
| Rule :     | Mandatory | Optional | Mandatory  | Optional |   Optional |

```
serverService.update_server("S4", new_port="25", new_address="bplanche@10.0.432.43", new_credentials=".ssh/path", new_alias="SS4")
```

Note that you are not obliged to modify all the fields in your line concerning the server you wish to modify. For example, you can only change the port by specifying `new_port` in addition to the mandatory `alias` in your update signature.

In addition, the server id cannot be modified; it may be generated automatically later.

4. #### Read

| Signature : |  alias_server  | 
| :---------- | -------------: |
| Type :      |   String       |
| Rule :     |   Mandatory    |


If you want to display a server by its alias, you can use the following command:
```
serverService.find_by_alias("SS4")
```

### Auto-Backup

First of all, instantiate the server service like this in `__main__.py` :

```
autoBackupService = AutoBackupService()
```

1. #### Creation

You can create an auto-backup with the following parameters:

| Signature : | id_backup | frequency |  name  | timestamp | id_server |   path |
| :---------- | :-------: | :-------: | :----: | :-------: | :-------: | -----: |
| Type :      |  String   |  String   | String |  String   |  String   | String |

Like this :

```
autoBackupService.create_auto_backup("9", "monthly", "okay", "2021-01-01", "3", "/home/backup")
```

2. #### Deleting

You can delete an auto-backup using its id as follows:
```
autoBackupService.delete_auto_backup("9")
```

3. #### Update

You can update an auto-backup using its id and these parameters:

| Signature : |  id_backup  | frequency  |    name    | timestamp  |       path |
| :---------- | :---------: | :--------: | :--------: | :--------: | ---------: |
| Type :      |   String    |   String   |   String   |   String   |     String |
| Rule :     | Mandatory | Optional | Optional | Optional | Optional |

```
autoBackupService.update_auto_backup("9", new_frequency="daily", new_timestamp="2021-01-02", new_path="/home/backup")
```

Please note that you are not obliged to change all the fields in your line concerning the auto-backup you wish to modify. For example, you can only change the name by specifying `new_name` in addition to the obligatory `id` in the signature of your update.

In addition, the id linked to the server cannot be modified, as the back-up is linked to it.

4. #### Read

| Signature : |  id_backup  | 
| :---------- | ----------: |
| Type :      |   String    |
| Rule :     | Mandatory |


If you want to display an auto-backup by its id, you can use the following command:

``
autoBackupService.find_by_id("9")
```

### Read the entire Auto-Backup & Server section

It is possible to display all servers or all auto-backups in our configuration file. To do this, use the following command:
```
autoBackupService.find_all()
or
serverService.find_all()
```