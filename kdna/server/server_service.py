"""This module contains the ServerService class."""
import os
import paramiko
from kdna.conf_utils.utils import Utils
import os


def create_dic_server(data):
    li = []
    for ligne in data:
        dic = {
            "id": ligne[0].strip(),
            "host": ligne[1].strip(),
            "path": ligne[2].strip(),
            "port": ligne[3].strip(),
            "alias": ligne[4].strip(),
        }
        li.append(dic)
    return li


class ServerService:
    def __int__(self):
        pass

    def get_max_id(self):
        """Get the maximum ID among the servers"""
        lines = self.find_all()
        max_id = 0
        for line in lines:
            if line[0] > max_id:
                max_id = line[0]
        return max_id

    def find_all(self):
        lines = Utils.read_file_lines(Utils.get_config_file_path())
        i = Utils.find_servers_index(lines) + 1
        index_autobackup = Utils.find_auto_backups_index(lines)
        data = [v.split(",") for v in lines[i:index_autobackup]]
        li = create_dic_server(data)

        return li

    def find_by_alias(self, alias):
        lines = Utils.read_file_lines(Utils.get_config_file_path())
        index_servers = Utils.find_servers_index(lines)
        index_auto_backups = Utils.find_auto_backups_index(lines)

        existing_aliases = self.extract_existing_aliases(
            lines, index_servers, index_auto_backups
        )
        if alias in existing_aliases:
            line_to_print = self.find_line_to_delete(
                lines, index_servers, alias, by_alias=True
            )
            print(lines[line_to_print].strip())
        else:
            print(
                f'Erreur : Aucun serveur trouvé avec l\'alias "{alias}" dans la '
                f"section [server]."
            )

    def create_server(self, id, address, credentials, port,  encrypt, alias):
        # On ouvre le fichier en mode lecture
        lines = Utils.read_file_lines(Utils.get_config_file_path())

        # On cherche la ligne contenant [server]
        index_servers = Utils.find_servers_index(lines)
        index_auto_backups = Utils.find_auto_backups_index(lines)

        if index_servers is not None:
            existing_servers = self.extract_existing_servers(
                lines, index_servers, index_auto_backups
            )

            if str(id) in existing_servers:
                print(
                    f'Erreur : L\'id du serveur "{id}" existe déjà dans la '
                    f"section [server]."
                )
                return

            # On vérifie de l'unicité de l'alias
            if alias is not None:
                existing_aliases = self.extract_existing_aliases(
                    lines, index_servers, index_auto_backups
                )
                if alias in existing_aliases:
                    print(f"Erreur : L'alias \"{alias}\" existe déjà dans la section ["
                          f"servers].")
                    return

            if encrypt != True and encrypt != False:
                print("Erreur : La valeur du paramètre encrypt doit être True ou False.")
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
            confirmation_message += " a été ajouté dans la section [server]."
            print(confirmation_message)
        else:
            print("Erreur : Section [server] non trouvé dans le fichier.")

    def delete_server(self, id: str, by_alias=False):
        lines = Utils.read_file_lines(Utils.get_config_file_path())
        index_servers = Utils.find_servers_index(lines)
        element_type = "alias" if by_alias else "id"
        if index_servers is None:
            print("Erreur : Section [server] non trouvée dans le fichier.")
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
                    f"section [server]."
                )
            # Sinon on affiche un message d'erreur
            else:
                print(
                    f'Erreur : Aucun élément trouvé avec l\'{element_type} "{id}" dans '
                    f"la section [server]."
                )
        # Sinon on affiche un message d'erreur
        else:
            if not by_alias and id == "None":
                print(
                    f'Erreur : Aucun élément trouvé avec l\'{element_type} "{id}" dans '
                    f"la section [server]."
                )

    def update_server(self, alias_to_update, new_path="", new_port="", new_address="", new_encrypt="",new_alias=""):
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
                existing_alias = existing_line[5].strip() if len(
                    existing_line) >= 5 else None

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
                    return

                # Construire la nouvelle ligne mise à jour
                updated_line = f"{existing_id}, {new_address}, {new_path}, {new_port}, {new_encrypt}, {new_alias}\n"

                # Mettre à jour la ligne
                lines[line_to_update] = updated_line

                # Écrire les lignes mises à jour dans le fichier
                with open(Utils.get_config_file_path(), "w", encoding="utf-8") as f:
                    f.writelines(lines)

                print(
                    f'Les informations du serveur avec l\'alias "{alias_to_update}" ont été '
                    f"mises à jour."
                )
            # Sinon, afficher un message d'erreur
            else:
                print(
                    f'Erreur : Aucun serveur trouvé avec l\'alias "{alias_to_update}" dans la '
                    f"section [server]."
                )
        # Sinon, afficher un message d'erreur
        else:
            print("Erreur : Section [server] non trouvée dans le fichier.")

    def import_server(self):
        """Import server from ~/.ssh/config file"""
        hosts = self.list_ssh_config_hosts()
        if hosts is None:
            print("Erreur : Fichier de configuration SSH non trouvé.")
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
            return None
        self.create_server(
            "R12",  # Temp value in wait of the increment insertion in create_server
            config_info["address"],
            config_info["credentials"],
            config_info["port"],
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
            f"l'{'alias' if by_alias else 'id'} \"{id}\" dans la section [server]."
        )
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
        if os.path.exists.expanduser("~/.ssh/config"):
            config_file = os.path.expanduser("~/.ssh/config")
            if not os.path.exists(config_file):
                return []
            with open(config_file, "r", encoding="utf-8") as file:
                lines = file.readlines()
            hosts = [line.split()[1] for line in lines if line.startswith("Host ")]
            return hosts
        else:
            return None

    @staticmethod
    def get_ssh_config_info(host):
        """Get the hostname and username from the SSH config file."""
        if os.path.exists.expanduser("~/.ssh/config"):
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
                print(
                    "Erreur : Aucune champ 'identityfile' trouvée dans le fichier de configuration."
                    )
                return None
            if "port" in user_config:
                cfg["port"] = user_config["port"]
            return cfg
        else:
            return None
