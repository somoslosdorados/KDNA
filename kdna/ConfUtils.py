class ConfUtils:
    # Fonctions utilitaires pour les fichiers de configuration
    config_file = 'config.txt'

    def initialize_config_file():
        config_content = "[servers]\n\n[auto-backups]\n"

        # On vérifie si le fichier existe déjà
        try:
            with open('config.txt', 'r') as f:
                content = f.read()
                # Si le fichier existe déjà et qu'il est correctement initialisé, on ne fait rien
                if "[servers]" in content and "[auto-backups]" in content:
                    return
        # On récupère l'erreur si le fichier n'existe pas
        except FileNotFoundError:
            print("Le fichier n'existe pas encore, nous allons le créer...")
            pass

        # On initialise le contenu du fichier de configuration si le fichier n'existe pas ou s'il n'est pas correctement initialisé
        with open('config.txt', 'w') as f:
            f.write(config_content)

        print("Le fichier de configuration a été initialisé avec succès.")

    @staticmethod
    def readAll():
        # Fonction pour afficher le fichier de configuration
        lines = ConfUtils.read_file_lines(ConfUtils.config_file)
        for line in lines:
            print(line.strip())

    @staticmethod
    def read_file_lines(filename):
        # Fonction pour lire les lignes d'un fichier
        with open(filename, 'r') as f:
            return f.readlines()

    @staticmethod
    def write_file_lines(filename, lines):
        # Fonction pour écrire les lignes dans un fichier
        with open(filename, 'w') as f:
            f.writelines(lines)

    @staticmethod
    def find_section(lines: list, pattern: str) -> int or None:
        """
        Fonction pour trouver l'indice d'une section
        """
        for i, line in enumerate(lines):
            if pattern in line:
                return i
        return None

    @staticmethod
    def find_auto_backups_index(lines):
        return ConfUtils.find_section(lines, "[auto-backups]")

    @staticmethod
    def find_servers_index(lines: list) -> int:
        """
        Fonction pour trouver l'indice de [servers]
        """
        return ConfUtils.find_section(lines, "[servers]")

    @staticmethod
    def delete_line(lines, line_to_delete):
        # Fonction pour supprimer une ligne
        del lines[line_to_delete]
