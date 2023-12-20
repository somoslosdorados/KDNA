"""Utils"""

CONFIG_TXT = 'kdna.conf'


class Utils:
    """Fonctions utilitaires pour les fichiers de configuration"""
    config_file = 'kdna.conf'

    @staticmethod
    def initialize_config_file():
        """Initialize the config file"""
        config_content = "[servers]\n[auto-backups]\n"

        # On vérifie si le fichier existe déjà
        try:
            with open(CONFIG_TXT, 'r', encoding="utf-8") as f:
                content = f.read()
                # Si le fichier existe déjà et qu'il est correctement initialisé, on ne fait rien
                if "[servers]" in content and "[auto-backups]" in content:
                    return
        # On récupère l'erreur si le fichier n'existe pas
        except FileNotFoundError:
            print("Le fichier n'existe pas encore, nous allons le créer...")
            pass

        # On initialise le contenu du fichier de configuration si le fichier n'existe pas ou
        # s'il n'est pas correctement initialisé
        with open(CONFIG_TXT, 'w', encoding="utf-8") as f:
            f.write(config_content)

        print("Le fichier de configuration a été initialisé avec succès.")

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
        with open(filename, 'r', encoding="utf-8") as f:
            return f.readlines()

    @staticmethod
    def write_file_lines(filename, lines):
        """Write a line in the config file"""
        # Fonction pour écrire les lignes dans un fichier
        with open(filename, 'w', encoding="utf-8") as f:
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
        """Find the index of a specific [servers]"""
        return Utils.find_section(lines, "[server]")

    @staticmethod
    def delete_line(lines, line_to_delete):
        """Delete a line in the config file"""
        del lines[line_to_delete]