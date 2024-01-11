"""Utils"""


import os


class Utils:
    """Fonctions utilitaires pour les fichiers de configuration"""

    config_file = "kdna.conf"

    @staticmethod
    def initialize_config_file():
        home_directory = os.path.expanduser("~")
        kdna_directory = os.path.join(home_directory, ".kdna")
        config_file_path = os.path.join(kdna_directory, Utils.config_file)
        config_content = "[server]\n[auto-backup]\n"
        # TODO: mettre les print dans les logs
        # Vérifier si le dossier kdna existe, sinon le créer
        if not os.path.exists(kdna_directory):
            os.makedirs(kdna_directory)
            # print("Dossier créé:", kdna_directory)
        else:
            # print("Le dossier existe déjà:", kdna_directory)
            pass

        # Vérifier si le fichier kdna.conf existe, sinon le créer
        if not os.path.exists(config_file_path):
            with open(config_file_path, "w") as config_file:
                config_file.write(config_content)
            # print("Fichier créé:", config_file_path)
        else:
            # print("Le fichier existe déjà:", config_file_path)
            pass

    @staticmethod
    def read_all():
        """Read all the configurations"""
        # Fonction pour afficher le fichier de configuration
        lines = Utils.read_file_lines(Utils.config_file)
        for line in lines:
            print(line.strip())

    @staticmethod
    def read_file_lines(filename):
        """Read a line of the file"""
        # Fonction pour lire les lignes d'un fichier
        with open(filename, "r", encoding="utf-8") as f:
            return f.readlines()

    @staticmethod
    def write_file_lines(filename, lines):
        """Write a line in the config file"""
        # Fonction pour écrire les lignes dans un fichier
        with open(filename, "w", encoding="utf-8") as f:
            f.writelines(lines)

    @staticmethod
    def find_section(lines: list, pattern: str):
        """Find a specific section in the config file"""
        for i, line in enumerate(lines):
            if pattern in line:
                return i
        return None

    @staticmethod
    def find_auto_backups_index(lines):
        """Find the index of a specific autobackup"""
        return Utils.find_section(lines, "[auto-backup]")

    @staticmethod
    def find_servers_index(lines: list) -> int:
        """Find the index of a specific [server]"""
        return Utils.find_section(lines, "[server]")

    @staticmethod
    def delete_line(lines, line_to_delete):
        """Delete a line in the config file"""
        del lines[line_to_delete]
