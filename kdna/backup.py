"""Backup"""
from kdna.conf_utils import ConfUtils


class Backup:
    """Class representing a backup"""
    def __init__(self, id_backup, frequency, name, timestamp, id_server, path):
        self.id_backup = id_backup
        self.frequency = frequency
        self.name = name
        self.timestamp = timestamp
        self.id_server = id_server
        self.path = path

    # Ajout d'une auto backup dans le fichier de configuration
    def add(self):
        """Add a new backup"""
        # On ouvre le fichier en mode lecture
        lines = ConfUtils.read_file_lines(ConfUtils.config_file)

        # On cherche les indices de [servers] et [auto-backups]
        index_servers = ConfUtils.find_servers_index(lines)
        index_auto_backups = ConfUtils.find_auto_backups_index(lines)

        # Vérification de l'existence de l'id_server dans la section [servers]
        if not self.check_id_server(lines, index_servers, index_auto_backups):
            print(
                f"Erreur : L'id du serveur \"{self.id_server}\" de votre auto backup n'existe "
                f"pas dans la section ["
                f"servers].")
            return

        # Construction de la nouvelle ligne
        new_line = (f"{self.id_backup}, {self.frequency}, {self.name}, {self.timestamp}, "
                    f"{self.id_server}, {self.path}\n")

        # Ajout de la ligne seulement si l'id_backup est unique
        existing_backups = self.extract_existing_backups(
            lines, index_auto_backups)
        if str(self.id_backup) in existing_backups:
            print(
                f"Erreur : L'id de l'auto backup \"{self.id_backup}\" existe déjà dans la "
                f"section [auto-backups].")
            return

        # Ajout de la ligne
        print(
            f"L'auto backup avec l'id \"{self.id_backup}\" a été ajouté dans la section ["
            f"auto-backups].")
        lines.insert(index_auto_backups + 1, new_line)

        # Écrire les lignes mises à jour dans le fichier
        with open(ConfUtils.config_file, 'w', encoding="utf-8") as f:
            f.writelines(lines)

    def check_id_server(self, lines, index_servers, index_auto_backups):
        """Check the id of a specific server"""
        # Fonction pour vérifier l'existence de l'id_server dans la section [servers]
        existing_servers = \
            [line.split(',')[0].strip() for line in lines[index_servers + 1:index_auto_backups] if
             len(line.split(',')) >= 4 and line.strip()]
        return str(self.id_server) in existing_servers

    @staticmethod
    def extract_existing_backups(lines, index_auto_backups):
        """Extract an existing backup"""
        # Fonction pour extraire les id_backup dans la section [auto-backups]
        return [line.split(',')[0].strip() for line in lines[index_auto_backups + 1:] if
                len(line.split(',')) >= 6 and line.strip()]

    # Suppression d'une auto backup dans le fichier de configuration
    @staticmethod
    def delete(id_to_delete):
        """Delete a backup"""
        # On ouvre le fichier en mode lecture
        lines = ConfUtils.read_file_lines(ConfUtils.config_file)

        # On cherche les indices de [servers] et [auto-backups]
        index_auto_backups = ConfUtils.find_auto_backups_index(lines)
        if index_auto_backups is None:
            print(
                "Erreur : Section [auto-backups] non trouvé dans le fichier.")
            return

        # On cherche la ligne à supprimer
        line_to_delete = Backup.find_line_to_delete(
            lines, index_auto_backups, id_to_delete)
        # Si la ligne à supprimer a été trouvée, on la supprime
        if line_to_delete is not None:
            ConfUtils.delete_line(lines, line_to_delete)
            ConfUtils.write_file_lines(ConfUtils.config_file, lines)
            print(
                f"L'auto backup avec l'id \"{id_to_delete}\" a été supprimé de la section ["
                f"auto-backups].")
        # Sinon on affiche un message d'erreur
        else:
            print(
                f"Erreur : Aucun élément trouvé avec l'id \"{id_to_delete}\" dans la section ["
                f"auto-backups].")

    @staticmethod
    def find_line_to_delete(lines, index_auto_backups, id_to_delete):
        """Function to find the line to delete"""
        for i, line in enumerate(lines[index_auto_backups + 1:]):
            if len(line.split(',')) >= 6 and line.strip():
                if line.split(',')[0].strip() == str(id_to_delete):
                    return i + index_auto_backups + 1
        return None

    @staticmethod
    def update(id_to_update, new_frequency=None, new_name=None, new_timestamp=None, new_path=None):
        """update a specific backup"""
        # On ouvre le fichier en mode lecture
        lines = ConfUtils.read_file_lines(ConfUtils.config_file)

        # On cherche les indices de [auto-backups]
        index_auto_backups = ConfUtils.find_auto_backups_index(lines)

        # On regarde si la section [auto-backups] existe
        if index_auto_backups is not None:
            # On cherche la ligne à mettre à jour
            line_to_update = Backup.find_line_to_update(
                lines, index_auto_backups, id_to_update)

            # Si la ligne à mettre à jour a été trouvée, on la met à jour
            if line_to_update is not None:
                # Récupérer les informations existantes
                existing_line = lines[line_to_update].strip().split(',')
                existing_id_backup = existing_line[0].strip()
                existing_frequency = existing_line[1].strip()
                existing_name = existing_line[2].strip()
                existing_timestamp = existing_line[3].strip()
                existing_id_server = existing_line[4].strip()
                existing_path = existing_line[5].strip() if len(
                    existing_line) >= 6 else None

                # Mettre à jour les informations si de nouvelles valeurs sont fournies
                new_frequency = new_frequency if new_frequency is not None else existing_frequency
                new_name = new_name if new_name is not None else existing_name
                new_timestamp = new_timestamp if new_timestamp is not None else existing_timestamp
                new_path = new_path if new_path is not None else existing_path

                # Construire la nouvelle ligne mise à jour
                updated_line = (f"{existing_id_backup}, {new_frequency}, {new_name}, "
                                f"{new_timestamp}, {existing_id_server}, {new_path}\n")

                # Mettre à jour la ligne
                lines[line_to_update] = updated_line

                # Écrire les lignes mises à jour dans le fichier
                with open(ConfUtils.config_file, 'w', encoding="utf-8") as f:
                    f.writelines(lines)

                print(
                    f"L'auto backup avec l'id \"{id_to_update}\" a été mis à jour dans la "
                    f"section [auto-backups].")
            # Sinon, afficher un message d'erreur
            else:
                print(
                    f"Erreur : Aucun élément trouvé avec l'id \"{id_to_update}\" dans la section "
                    f"[auto-backups].")
        else:
            print(
                "Erreur : Section [auto-backups] non trouvée dans le fichier.")

    @staticmethod
    def find_line_to_update(lines, index_auto_backups, id_to_update):
        """find the line to update"""
        # Fonction pour trouver la ligne à mettre à jour
        auto_backups_lines = lines[index_auto_backups + 1:]

        for i, line in enumerate(auto_backups_lines):
            if len(line.split(',')) >= 6 and line.strip():
                line_id = line.split(',')[0].strip()

                # Si l'id correspond à celui à mettre à jour
                if line_id == str(id_to_update):
                    return i + index_auto_backups + 1

        return None
