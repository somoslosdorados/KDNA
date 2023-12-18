from ConfUtils import ConfUtils


class Server:
    def __init__(self, id_server, credentials, port, alias):
        self.id_server = id_server
        self.credentials = credentials
        self.port = port
        self.alias = alias

    # Ajout d'un serveur dans le fichier de configuration
    def add(self):

        # On ouvre le fichier en mode lecture
        lines = ConfUtils.read_file_lines(ConfUtils.config_file)

        # On cherche la ligne contenant [servers]
        index_servers = ConfUtils.find_servers_index(lines)
        index_auto_backups = ConfUtils.find_auto_backups_index(lines)

        # On regarde si la ligne contenant [servers] a été trouvée
        if index_servers is None:
            print("Erreur : Section [servers] non trouvée dans le fichier.")
            return

        # On vérifie l'unicité de l'id_server dans la section [servers]
        existing_servers = self.extract_existing_servers(
            lines, index_servers, index_auto_backups)
        if str(self.id_server) in existing_servers:
            print(
                f"Erreur : L'id du serveur \"{self.id_server}\" existe déjà dans la section [servers].")
            return

        # On vérifie de l'unicité de l'alias
        if self.alias is not None:
            existing_aliases = self.extract_existing_aliases(
                lines, index_servers, index_auto_backups)
            if self.alias in existing_aliases:
                print(
                    f"Erreur : L'alias \"{self.alias}\" existe déjà dans la section [servers].")
                return

        # Construction de la nouvelle ligne
        new_line = f"{self.id_server}, {self.credentials}, {self.port}, {self.alias}\n"

        # Ajout de la ligne seulement si l'id_server et l'alias sont uniques
        lines.insert(index_servers + 1, new_line)

        # Écrire les lignes mises à jour dans le fichier
        with open(ConfUtils.config_file, 'w') as f:
            f.writelines(lines)
        confirmation_message = f"Le serveur avec l'id \"{self.id_server}\""
        if self.alias is not None:
            confirmation_message += f" et l'alias \"{self.alias}\""
        confirmation_message += " a été ajouté dans la section [servers]."
        print(confirmation_message)
        # Sinon on affiche un message d'erreur

    # Suppression d'un serveur dans le fichier de configuration
    @staticmethod
    def delete(id_or_alias, by_alias=False):
        lines = ConfUtils.read_file_lines(ConfUtils.config_file)
        index_servers = ConfUtils.find_servers_index(lines)
        element_type = 'alias' if by_alias else 'id'
        if index_servers is None:
            print("Erreur : Section [servers] non trouvée dans le fichier.")
            return

        line_to_delete = Server.find_line_to_delete(
            lines, index_servers, id_or_alias, by_alias)

        # Si la ligne à supprimer a été trouvée, on la supprime
        if line_to_delete is not None:
            deleted_line = lines[line_to_delete].strip()
            line_elements = deleted_line.split(',')

            # On vérifie que la ligne contient au moins 4 éléments et qu'elle n'est pas vide
            if len(line_elements) >= 4 and deleted_line.strip():
                # On supprime la ligne
                ConfUtils.delete_line(lines, line_to_delete)
                ConfUtils.write_file_lines(ConfUtils.config_file, lines)
                # On affiche un message de confirmation
                print(
                    f"L'élément avec l'{element_type} {id_or_alias} a été supprimé de la section [servers].")
            # Sinon on affiche un message d'erreur
            else:
                print(
                    f"Erreur : Aucun élément trouvé avec l'{element_type} \"{id_or_alias}\" dans la section [servers].")
        # Sinon on affiche un message d'erreur
        else:
            if not by_alias and id_or_alias == 'None':
                print(
                    f"Erreur : Aucun élément trouvé avec l'{element_type} \"{id_or_alias}\" dans la section [servers].")

    @staticmethod
    def extract_existing_servers(lines, index_servers, index_auto_backups):
        # Fonction pour extraire les id_server dans la section [servers]
        return [line.split(',')[0].strip() for line in lines[index_servers + 1:index_auto_backups] if len(line.split(',')) >= 4 and line.strip()]

    @staticmethod
    def extract_existing_aliases(lines, index_servers, index_auto_backups):
        # Fonction pour extraire les aliases dans la section [servers]
        return [line.split(',')[3].strip() if len(line.split(',')) >= 4 else None for line in lines[index_servers + 1:index_auto_backups] if line.strip()]

    @staticmethod
    def find_line_to_delete(lines, index_servers, id_or_alias, by_alias=False):
        # Fonction pour trouver la ligne à supprimer
        index_auto_backups = ConfUtils.find_auto_backups_index(lines)
        if index_auto_backups is None:
            index_auto_backups = len(lines)
        server_lines = lines[index_servers + 1:index_auto_backups]

        for i, line in enumerate(server_lines):
            if len(line.split(',')) >= 4 and line.strip():
                line_id = line.split(',')[0].strip()
                line_alias = line.split(',')[3].strip() if len(
                    line.split(',')) >= 4 else None

                if by_alias and line_alias == id_or_alias or not by_alias and line_id == str(id_or_alias):
                    return i + index_servers + 1
        print(
            f"Erreur : Aucun élément trouvé avec l'{'alias' if by_alias else 'id'} \"{id_or_alias}\" dans la section [servers].")
        return None

    @staticmethod
    def update(alias_to_update, new_credentials=None, new_port=None, new_alias=None):
        # On ouvre le fichier en mode lecture
        lines = ConfUtils.read_file_lines(ConfUtils.config_file)

        # On cherche la ligne contenant [servers]
        index_servers = ConfUtils.find_servers_index(lines)

        # On regarde si la ligne contenant [servers] a été trouvée
        if index_servers is not None:
            # On cherche la ligne à mettre à jour
            line_to_update = Server.find_line_to_update(
                lines, index_servers, alias_to_update)

            # Si la ligne à mettre à jour a été trouvée, on la met à jour
            if line_to_update is not None:
                # Récupérer les informations existantes
                existing_line = lines[line_to_update].strip().split(',')
                existing_id = existing_line[0].strip()
                existing_credentials = existing_line[1].strip()
                existing_port = existing_line[2].strip()
                existing_alias = existing_line[3].strip() if len(
                    existing_line) >= 4 else None

                # Mettre à jour les informations si de nouvelles valeurs sont fournies
                new_credentials = new_credentials if new_credentials is not None else existing_credentials
                new_port = new_port if new_port is not None else existing_port

                # Vérifier si le nouvel alias existe déjà
                if new_alias is not None and new_alias != existing_alias and new_alias in Server.extract_existing_aliases(lines, index_servers, len(lines)):
                    print(
                        "Erreur : Le nouvel alias existe déjà dans la liste des serveurs.")
                    return

                # Construire la nouvelle ligne mise à jour
                updated_line = f"{existing_id}, {new_credentials}, {new_port}, {new_alias}\n"

                # Mettre à jour la ligne
                lines[line_to_update] = updated_line

                # Écrire les lignes mises à jour dans le fichier
                with open(ConfUtils.config_file, 'w') as f:
                    f.writelines(lines)

                print(
                    f"Les informations du serveur avec l'alias \"{alias_to_update}\" ont été mises à jour.")
            # Sinon, afficher un message d'erreur
            else:
                print(
                    f"Erreur : Aucun serveur trouvé avec l'alias \"{alias_to_update}\" dans la section [servers].")
        # Sinon, afficher un message d'erreur
        else:
            print("Erreur : Section [servers] non trouvée dans le fichier.")

    @staticmethod
    def find_line_to_update(lines, index_servers, alias_to_update):
        # Fonction pour trouver la ligne à mettre à jour
        index_auto_backups = ConfUtils.find_auto_backups_index(lines)
        if index_auto_backups is None:
            index_auto_backups = len(lines)
        server_lines = lines[index_servers + 1:index_auto_backups]

        for i, line in enumerate(server_lines):
            if len(line.split(',')) >= 4 and line.strip():
                line_id = line.split(',')[0].strip()
                line_alias = line.split(',')[3].strip() if len(
                    line.split(',')) >= 4 else None

                # Si l'alias correspond à celui à mettre à jour
                if line_alias == alias_to_update:
                    return i + index_servers + 1

        return None
