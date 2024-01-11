from kdna.conf_utils.utils import Utils

class AutoBackupService:
  def __int__(self):
    pass

  def find_all(self):
    lines = Utils.read_file_lines(Utils.config_file)
    i = Utils.find_auto_backups_index(lines) + 1
    endfile = len(lines)
    while(i != endfile):
        print(lines[i].strip())
        i += 1   

  def find_by_id(self, id):
    lines = Utils.read_file_lines(Utils.config_file)
    i = Utils.find_auto_backups_index(lines)
    endfile = len(lines)
    while(i != endfile):
      if id == lines[i].split(',')[0].strip():
        print(lines[i])
      i += 1 
  
  def create_auto_backup(self, id, frequency, name, timestamp, id_server, path):
    """Add a new backup"""
    # On ouvre le fichier en mode lecture
    lines = Utils.read_file_lines(Utils.config_file)

    # On cherche les indices de [server] et [auto-backup]
    index_servers = Utils.find_servers_index(lines)
    index_auto_backups = Utils.find_auto_backups_index(lines)

    # Vérification de l'existence de l'id_server dans la section [server]
    if not self.check_id_server(lines, index_servers, index_auto_backups, id_server):
        print(
            f"Erreur : L'id du serveur \"{id_server}\" de votre auto backup n'existe "
            f"pas dans la section ["
            f"servers].")
        return

    # Construction de la nouvelle ligne
    new_line = (f"{id}, {frequency}, {name}, {timestamp}, "
                f"{id_server}, {path}\n")

    # Ajout de la ligne seulement si l'id_backup est unique
    existing_backups = self.extract_existing_backups(
        lines, index_auto_backups)
    if str(id) in existing_backups:
        print(
            f"Erreur : L'id de l'auto backup \"{id}\" existe déjà dans la "
            f"section [auto-backup].")
        return

    # Ajout de la ligne
    print(
        f"L'auto backup avec l'id \"{id}\" a été ajouté dans la section ["
        f"auto-backups].")
    lines.insert(index_auto_backups + 1, new_line)

    # Écrire les lignes mises à jour dans le fichier
    with open(Utils.config_file, 'w', encoding="utf-8") as f:
        f.writelines(lines)
        
  def delete_auto_backup(self, id):
    """Delete a backup"""
    # On ouvre le fichier en mode lecture
    lines = Utils.read_file_lines(Utils.config_file)

    # On cherche les indices de [server] et [auto-backup]
    index_auto_backups = Utils.find_auto_backups_index(lines)
    if index_auto_backups is None:
        print(
            "Erreur : Section [auto-backup] non trouvé dans le fichier.")
        return

    # On cherche la ligne à supprimer
    line_to_delete = self.find_line_to_delete(
        lines, index_auto_backups, id)
    # Si la ligne à supprimer a été trouvée, on la supprime
    if line_to_delete is not None:
        Utils.delete_line(lines, line_to_delete)
        Utils.write_file_lines(Utils.config_file, lines)
        print(
            f"L'auto backup avec l'id \"{id}\" a été supprimé de la section ["
            f"auto-backups].")
    # Sinon on affiche un message d'erreur
    else:
        print(
            f"Erreur : Aucun élément trouvé avec l'id \"{id}\" dans la section ["
            f"auto-backups].")
        
  def update_auto_backup(self, id, new_frequency=None, new_name=None, new_timestamp=None, new_path=None):
    """update a specific backup"""
    # On ouvre le fichier en mode lecture
    lines = Utils.read_file_lines(Utils.config_file)

    # On cherche les indices de [auto-backup]
    index_auto_backups = Utils.find_auto_backups_index(lines)

    # On regarde si la section [auto-backup] existe
    if index_auto_backups is not None:
        # On cherche la ligne à mettre à jour
        line_to_update = self.find_line_to_update(
            lines, index_auto_backups, id)

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
            with open(Utils.config_file, 'w', encoding="utf-8") as f:
                f.writelines(lines)

            print(
                f"L'auto backup avec l'id \"{id}\" a été mis à jour dans la "
                f"section [auto-backup].")
        # Sinon, afficher un message d'erreur
        else:
            print(
                f"Erreur : Aucun élément trouvé avec l'id \"{id}\" dans la section "
                f"[auto-backup].")
    else:
        print(
            "Erreur : Section [auto-backup] non trouvée dans le fichier.")

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
        
  def check_id_server(self, lines, index_servers, index_auto_backups, id_server):
    """Check the id of a specific server"""
    # Fonction pour vérifier l'existence de l'id_server dans la section [server]
    existing_servers = \
        [line.split(',')[0].strip() for line in lines[index_servers + 1:index_auto_backups] if
          len(line.split(',')) >= 4 and line.strip()]
    return str(id_server) in existing_servers
  
  @staticmethod
  def extract_existing_backups(lines, index_auto_backups):
    """Extract an existing backup"""
    # Fonction pour extraire les id_backup dans la section [auto-backup]
    return [line.split(',')[0].strip() for line in lines[index_auto_backups + 1:] if
            len(line.split(',')) >= 6 and line.strip()]
    
  @staticmethod
  def find_line_to_delete(lines, index_auto_backups, id_to_delete):
    """Function to find the line to delete"""
    for i, line in enumerate(lines[index_auto_backups + 1:]):
        if len(line.split(',')) >= 6 and line.strip():
            if line.split(',')[0].strip() == str(id_to_delete):
                return i + index_auto_backups + 1
    return None