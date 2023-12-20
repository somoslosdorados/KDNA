import json
from fabric import Connection # type: ignore
from typing import Union
import subprocess

# def get_json_connection_informations() -> Union[None, dict]:
#     """
#     get all conection informations from a JSON file.
#     """
#     json_file_name = "kdna/env.json"
#     try:
#         with open(json_file_name, 'r') as file:
#             data = json.load(file)

#             if "server_ip" not in data or data['server_ip'] is None:
#                 print("Veuillez spécifier l'adresse ip de l'hôte.")
#                 return None

#             elif "user_name" not in data or data['user_name'] is None:
#                 print("Veuillez spécifier votre nom utilisateur sur le serveur distant.")
#                 return None

#             elif "ssh_key" not in data or data['ssh_key'] is None:
#                 user_name = ""
#                 result = subprocess.run(['ls', '/home'], check=True, text=True, capture_output=True)
#                 user_names = result.stdout.split('\n')[:-1]
#                 # Si l'ordinateur local possède plusieurs utilisateurs
#                 if len(user_names) > 1:
#                     for name in user_names:
#                         print("- " + name)
#                     while user_name not in user_names:
#                         user_name = input("Votre ordinateur local possède plusieurs utilisateurs, veuillez préciser lequel possède la clé SSH permettant de se connecter au serveur distant : ")
#                     print(" ")
#                 else:
#                     user_name = user_names[0]

#                 result = subprocess.run('ls /home/' + user_name + '/.ssh/ | grep "^id_" | grep -v ".pub$"', shell=True, check=True, text=True, capture_output=True)
#                 private_key = ""
#                 private_keys = result.stdout.split('\n')[:-1]

#                 # Si l'ordinateur local possède plusieurs clés privées
#                 if len(private_keys) > 1:
#                     for key in private_keys:
#                         print("- " + key)
#                     while private_key not in private_keys:
#                         private_key = input("Votre ordinateur local possède plusieurs clés privées, veuillez préciser laquelle vous souhaitez utiliser pour vous connecter au serveur distant : ")
#                     print(" ")
#                 elif len(private_keys) == 0:
#                     print("Aucune clé privée n'a été trouvée, la connection au serveur distant ne peut pas se poursuivre.")
#                     return None
#                 else:
#                     private_key = private_keys[0]

#                 return {
#                     'host': data['server_ip'],
#                     'user': data['user_name'],
#                     'connect_kwargs': {
#                         "key_filename": "/home/" + user_name + "/.ssh/" + private_key
#                     }
#                 }

#             return {
#                 'host': data['server_ip'],
#                 'user': data['user_name'],
#                 'connect_kwargs': {
#                     "key_filename": data['ssh_key']
#                 }
#             }
#     except:
#         print("Veuillez créer un fichier '" + json_file_name + "'.")
#         return None

# def list_folders(connection: Connection, path: str) -> Union[None, list]:
#     """
#     list all files and folders in a specific path.
#     """
#     try:
#         repertoire_courant = connection.run('ls ' + path, hide=True)
#         return repertoire_courant.stdout.split('\n')[:-1]
#     except:
#         return None

# def create_folder(connection: Connection, path: str, folder_name: str) -> bool:
#     """
#     create a file on a specific path in the remote server.
#     """
#     try:
#         connection.run('mkdir ' + path + folder_name, hide=True)
#         return True
#     except:
#         return False

def send_file(connection: Connection, local_path: str, remote_path: str) -> bool:
    """
    send a file on a specific path in the remote server.
    """
    try:
        connection.put(local_path, remote=remote_path)
        return True
    except:
        return False

# def main():
#     connection_param = get_json_connection_informations()
#     if connection_param is None:
#         print("Une erreur est survenue lors de la connexion au serveur.")
#         exit(1)

#     with Connection(**connection_param) as c:
#         repertories = list_folders(c, './')
#         if repertories is None:
#             print("Une erreur est survenue de l'execution de la fonction 'list_folders'.")
#             exit(1)

#         if "kdna" not in repertories:
#             print("Création du répertoire 'kdna'")
#             state_creation = create_folder(c, './', "kdna")

#             if not state_creation:
#                 print("--- Une erreur est survenue lors de création du répertoire 'kdna' ---")
#                 exit(1)

#         print("Envoi du fichier 'my_file.txt'")
#         state_send = send_file(c, './', 'kdna/my_file.txt', './kdna/')
#         if not state_send:
#             print("--- Une erreur est survenue de l'envoi du fichier ---")
#         else:
#             print("OK")

def main ():
    with Connection("bbronsin@168.38.112.136") as c:
        send_file(c, "/home/baptiste/Bureau/toto.txt", "/kdna/projet1/")

if __name__ == '__main__':
    main()