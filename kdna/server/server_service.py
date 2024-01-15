# mypy: ignore-errors
"""This module contains the ServerService class."""
import os
import paramiko
from kdna.conf_utils.utils import Utils
from kdna.logger.logger import log
from kdna.server.server import Server


def array_to_dic(array):
  return {
    'id': array[0].strip(),
    'host': array[1].strip(),
    'path': array[2].strip(),
    'port': array[3].strip(),
    'alias': array[4].strip()
  }

def create_dic_server(data):
    """Create a dictionnary with the data of the server"""
    li = []
    for ligne in data:
        dic = {
            "id": ligne[0].strip(),
            "host": ligne[1].strip(),
            "path": ligne[2].strip(),
            "port": ligne[3].strip(),
            "encrypt": ligne[4].strip(),
            "alias": ligne[5].strip(),
        }
        li.append(dic)
    return li


class ServerService:
    """This class contains the methods to manage the servers."""

    def __int__(self):
        pass

    def get_max_id(self):
        """Get the maximum ID among the servers"""
        lines = self.find_all()
        max_id = 0
        # # for line in lines:
        # #     if line[0] > max_id:
        # #         max_id = line[0]
        for server in lines:
            if server['id'] > max_id:
                max_id = server['id']
        for server in lines:
            if int(server['id']) > max_id:
                max_id = int(server['id'])
        return max_id

    def find_all(self):
        """Find all the servers in the config file"""
        lines = Utils.read_file_lines(Utils.get_config_file_path())
        i = Utils.find_servers_index(lines) + 1
        index_autobackup = Utils.find_auto_backups_index(lines)
        data = [v.split(",") for v in lines[i:index_autobackup]]
        li = create_dic_server(data)

        return li

    def find_by_alias(self, alias):
        """Find a server by his alias"""
        lines = Utils.read_file_lines(Utils.get_config_file_path())
        index_servers = Utils.find_servers_index(lines)
        index_auto_backups = Utils.find_auto_backups_index(lines)
        lines = Utils.read_file_lines(Utils.get_config_file_path())
        index_servers = Utils.find_servers_index(lines)
        index_auto_backups = Utils.find_auto_backups_index(lines)

        existing_aliases = self.extract_existing_aliases(
            lines,
            index_servers,
            index_auto_backups
        )
        if alias in existing_aliases:
            line_to_print = self.find_line_to_delete(lines, index_servers, alias, by_alias=True)
            #print(lines[line_to_print].strip())
            data_server = array_to_dic(lines[line_to_print].split(','))
            server = Server(data_server['host'])
            return server

        else:
            print(f"Erreur : Aucun serveur trouvé avec l'alias \"{alias}\" dans la "
                f"section [servers].")

    def create_server(self, id, address, credentials, port,  encrypt, alias):
        # On ouvre le fichier en mode lecture
        lines = Utils.read_file_lines(Utils.get_config_file_path())

        # On cherche la ligne contenant [servers]
        index_servers = Utils.find_servers_index(lines)
        index_auto_backups = Utils.find_auto_backups_index(lines)

        if index_servers is not None:
            existing_servers = self.extract_existing_servers(
                lines, index_servers, index_auto_backups
            )

            if str(id) in existing_servers:
                print(
                    f'Erreur : L\'id du serveur "{id}" existe déjà dans la '
                    f"section [servers]."
                )
                log("ERROR", "Erreur : L\'id du serveur " + id + " existe déjà dans la"
                                                                   " section [servers].")
                return

            if id != "":
                id = int(id)
            else:
                id = self.get_max_id() + 1
            # On vérifie de l'unicité de l'alias
            if alias is not None:
                existing_aliases = self.extract_existing_aliases(
                    lines, index_servers, index_auto_backups
                )
                if alias in existing_aliases:
                    print(f"Erreur : L'alias " + alias + " existe déjà dans la section ["
                          f"servers].")
                    log("ERROR", "Erreur : L'alias " + alias + " existe déjà dans la "
                                                                 "section [servers].")
                    log("ERROR", "Erreur : L'alias " + alias + " existe déjà dans la "
                                                                 "section [servers].")
                    return

            if encrypt not in (True, False):
                print("Erreur : La valeur du paramètre encrypt doit être True ou False.")
                log("ERROR", "Erreur : La valeur du paramètre encrypt doit être "
                             "True ou False.")
                log("ERROR", "Erreur : La valeur du paramètre encrypt doit être True "
                             "ou False.")
                return

            # Construction de la nouvelle ligne
            new_line = f"{id}, {address}, {credentials}, {port}, {encrypt}, {alias}\n"

            # Ajout de la ligne seulement si l'id_server et l'alias sont uniques
            lines.insert(index_servers + 1, new_line)

            with open(Utils.get_config_file_path(), "w", encoding="utf-8") as f:
                f.writelines(lines)
            confirmation_message = f'Le server avec l\'id "{id}"'
            if alias is not None:
                confirmation_message += f'et l\'alias "{alias}"'
            confirmation_message += " a été ajouté dans la section [servers]."
            print(confirmation_message)
            log("INFO", confirmation_message)
            log("INFO", confirmation_message)
        else:
            print("Erreur : Section [servers] non trouvé dans le fichier.")
            log("ERROR", "Erreur : Section [servers] non trouvé dans le fichier.")

    def delete_server(self, id: str, by_alias=False):
        """Delete a server in the config file"""
        lines = Utils.read_file_lines(Utils.get_config_file_path())
        index_servers = Utils.find_servers_index(lines)
        element_type = "alias" if by_alias else "id"
        if index_servers is None:
            print("Erreur : Section [servers] non trouvée dans le fichier.")
            log("ERROR", "Erreur : Section [servers] non trouvée dans le fichier.")
            return

        line_to_delete = self.find_line_to_delete(lines, index_servers, id, by_alias)

        if line_to_delete is not None:
            deleted_line = lines[line_to_delete].strip()
            line_elements = deleted_line.split(",")

            # On vérifie que la ligne contient au moins 4 éléments et qu'elle n'est pas vide
            if len(line_elements) >= 4 and deleted_line.strip():
                # On supprime la ligne
                Utils.delete_line(lines, line_to_delete)
                Utils.write_file_lines(Utils.get_config_file_path(), lines)
                # On affiche un message de confirmation
                print(
                    f"L'élément avec l'{element_type} {id} a été supprimé de la "
                    f"section [servers]."
                )
                log("INFO", "L'élément avec l\'" + element_type + id + "a été "
                                                               "supprimé de la section [servers].")
            # Sinon on affiche un message d'erreur
            else:
                print(
                    f'Erreur : Aucun élément trouvé avec l\'{element_type} "{id}" dans '
                    f"la section [servers]."
                )
                log("ERROR", "Erreur : Aucun élément trouvé avec l\'" + element_type +
                    id + "dans la section [servers].")
        # Sinon on affiche un message d'erreur
        else:
            if not by_alias and id == "None":
                print(
                    f'Erreur : Aucun élément trouvé avec l\'{element_type} "{id}" dans '
                    f"la section [servers]."
                )
                log("ERROR", "Erreur : Aucun élément trouvé avec l\'" + element_type +
                    id + "dans la section [servers].")

    def update_server(
        self,
        alias_to_update,
        new_path="",
        new_port="",
        new_address="",
        new_encrypt="",
        new_alias="",
    ):
        """Update a server in the config file"""
        lines = Utils.read_file_lines(Utils.get_config_file_path())

        index_servers = Utils.find_servers_index(lines)

        if index_servers is not None:
            # On cherche la ligne à mettre à jour
            line_to_update = self.find_line_to_update(
                lines, index_servers, alias_to_update
            )

            # Si la ligne à mettre à jour a été trouvée, on la met à jour
            if line_to_update is not None:
                # Récupérer les informations existantes
                existing_line = lines[line_to_update].strip().split(",")
                existing_id = existing_line[0].strip()
                existing_address = existing_line[1].strip()
                existing_path = existing_line[2].strip()
                existing_port = existing_line[3].strip()
                existing_encrypt = existing_line[4].strip()
                existing_alias = (
                    existing_line[5].strip() if len(existing_line) >= 5 else None
                )

                # Mettre à jour les informations si de nouvelles valeurs sont fournies
                new_address = new_address if new_address != "" else existing_address
                new_path = new_path if new_path != "" else existing_path
                new_port = new_port if new_port != "" else existing_port
                new_alias = new_alias if new_alias != "" else existing_alias
                new_encrypt = new_encrypt if new_encrypt != "" else existing_encrypt

                # Vérifier si le nouvel alias  existe déjà
                if (
                    new_alias is not None
                    and new_alias != existing_alias
                    and new_alias
                    in self.extract_existing_aliases(lines, index_servers, len(lines))
                ):
                    print(
                        "Erreur : Le nouvel alias existe déjà dans la liste des serveurs."
                    )
                    log("ERROR", "Erreur : Le nouvel alias existe déjà dans la liste"
                                 " des serveurs.")
                    log("ERROR", "Erreur : Le nouvel alias existe déjà dans la liste"
                                 " des serveurs.")
                    return

                # Construire la nouvelle ligne mise à jour
                updated_line = (f"{existing_id}, {new_address}, {new_path}, {new_port}, "
                                f"{new_encrypt}, {new_alias}\n")

                # Mettre à jour la ligne
                lines[line_to_update] = updated_line

                # Écrire les lignes mises à jour dans le fichier
                with open(Utils.get_config_file_path(), "w", encoding="utf-8") as f:
                    f.writelines(lines)

                print(
                    f'Les informations du serveur avec l\'alias "{alias_to_update}" ont été '
                    f"mises à jour."
                )
                log("INFO", "Les informations du serveur avec l\'alias " +
                    alias_to_update + " ont été mises à jour.")
            # Sinon, afficher un message d'erreur
            else:
                print(
                    f'Erreur : Aucun serveur trouvé avec l\'alias "{alias_to_update}" dans la '
                    f"section [servers]."
                )
                log("ERROR", "Erreur : Aucun serveur trouvé avec l\'alias " +
                    alias_to_update + " dans la section [servers].")
        # Sinon, afficher un message d'erreur
        else:
            print("Erreur : Section [servers] non trouvée dans le fichier.")
            log("ERROR", "Erreur : Section [servers] non trouvée dans le fichier.")

    def import_server(self):
        """Import server from ~/.ssh/config file"""
        hosts = self.list_ssh_config_hosts()
        if hosts is None:
            print("Erreur : Fichier de configuration SSH non trouvé.")
            log("ERROR", "Erreur : Fichier de configuration SSH non trouvé.")
            return None
        print("------------------------------")
        print("Available hosts:")
        for i, host in enumerate(hosts):
            print(f"{i + 1}. {host}")
        print("---------------")
        choice = int(input("Select a host number: ")) - 1
        print("------------------------------")
        config_info = self.get_ssh_config_info(hosts[choice])
        if config_info is None:
            print("Erreur : Fichier de configuration SSH non trouvé.")
            log("ERROR", "Erreur : Fichier de configuration SSH non trouvé.")
            log("ERROR", "Erreur : Fichier de configuration SSH non trouvé.")
            return None
        
        encrypt = input("Encrypt the backups (Y/n): ")
        if encrypt == "y":
            encrypt = True
        elif encrypt == "n":
            encrypt = False
        else:
            encrypt = True
            
        self.create_server(
            "",
            config_info["address"],
            config_info["credentials"],
            config_info["port"],
            encrypt,
            config_info["alias"],
        )
        return None

    @staticmethod
    def extract_existing_servers(lines, index_servers, index_auto_backups):
        """Extract the id of th server"""
        return [
            line.split(",")[0].strip()
            for line in lines[index_servers + 1 : index_auto_backups]
            if len(line.split(",")) >= 4 and line.strip()
        ]

    @staticmethod
    def extract_existing_aliases(lines, index_servers, index_auto_backups):
        """Extract the aliases in the server section"""
        return [
            line.split(",")[5].strip() if len(line.split(",")) >= 6 else None
            for line in lines[index_servers + 1 : index_auto_backups]
            if line.strip()
        ]

    @staticmethod
    def find_line_to_delete(lines, index_servers, id, by_alias=False):
        """Find the line to delete"""
        index_auto_backups = Utils.find_auto_backups_index(lines)
        if index_auto_backups is None:
            index_auto_backups = len(lines)
        server_lines = lines[index_servers + 1 : index_auto_backups]

        for i, line in enumerate(server_lines):
            if len(line.split(",")) >= 6 and line.strip():
                line_id = line.split(",")[0].strip()
                line_alias = (
                    line.split(",")[5].strip() if len(line.split(",")) >= 6 else None
                )

                if by_alias and line_alias == id or not by_alias and line_id == str(id):
                    return i + index_servers + 1
        print(
            f"Erreur : Aucun élément trouvé avec "
            f"l'{'alias' if by_alias else 'id'} \"{id}\" dans la section [servers]."
        )
        log("ERROR", "Erreur : Aucun élément trouvé dans la section [servers].")
        return None

    @staticmethod
    def find_line_to_update(lines, index_servers, alias_to_update):
        """Find the line to update"""
        index_auto_backups = Utils.find_auto_backups_index(lines)
        if index_auto_backups is None:
            index_auto_backups = len(lines)
        server_lines = lines[index_servers + 1 : index_auto_backups]

        for i, line in enumerate(server_lines):
            if len(line.split(",")) >= 6 and line.strip():
                line.split(",")[0].strip()
                line_alias = (
                    line.split(",")[5].strip() if len(line.split(",")) >= 6 else None
                )

                # Si l'alias correspond à celui à mettre à jour
                if line_alias == alias_to_update:
                    return i + index_servers + 1
        return None

    @staticmethod
    def list_ssh_config_hosts():
        """
        List all hosts in the SSH config file.
        """
        if os.path.exists(os.path.expanduser("~/.ssh/config")):
            config_file = os.path.expanduser("~/.ssh/config")
            if not os.path.exists(config_file):
                return []
            with open(config_file, "r", encoding="utf-8") as file:
                lines = file.readlines()
            hosts = [line.split()[1] for line in lines if line.startswith("Host ")]
            return hosts
        return None

    @staticmethod
    def get_ssh_config_info(host):
        """Get the hostname and username from the SSH config file."""
        if os.path.exists(os.path.expanduser("~/.ssh/config")):
            config = paramiko.SSHConfig()
            user_config_file = os.path.expanduser("~/.ssh/config")
            if os.path.exists(user_config_file):
                with open(user_config_file, encoding="utf-8") as f:
                    config.parse(f)
            cfg = {"alias": host, "address": None, "port": 22, "credentials": None}
            user_config = config.lookup(host)
            if "hostname" in user_config:
                cfg["address"] = user_config["user"] + "@" + user_config["hostname"]
            if "identityfile" in user_config:
                cfg["credentials"] = user_config["identityfile"][0]
            else:
                if os.path.exists(os.path.expanduser("~/.ssh/id_rsa")):
                    cfg["credentials"] = os.path.expanduser("~/.ssh/id_rsa")
                    print(
                        "You dosent's have IdentityFile field in your ssh config file, we use the"
                        " default key (id_rsa)."
                    )
                else:
                    print(
                        "Error: You dosent's have IdentityFile field in your ssh config file, and"
                        " no default key (id_rsa)."
                    )
                log ("ERROR", "Erreur : Aucune champ 'identityfile' trouvée dans le"
                              " fichier de configuration.")
                log ("ERROR", "Erreur : Aucune champ 'identityfile' trouvée dans le"
                              " fichier de configuration.")
                return None
            if "port" in user_config:
                cfg["port"] = user_config["port"]
            return cfg
        return None
