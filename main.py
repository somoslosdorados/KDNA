import subprocess
import time

def start_systemd_service(service_name):
  try:  # Commandes d'activation du service (il sera lancé automatiquement au démarrage) et de renvoi du statut
    subprocess.run(['systemctl', 'start', service_name], check=True)
    subprocess.run(['systemctl', 'status', service_name], check=True)
    print(f"Cadéna attaché avec sukesé : Service '{service_name}' started successfully.")
  except subprocess.CalledProcessError as err:
    print(f"Impossible d'attacher le cadéna - Error starting service '{service_name}': {err}")


def main():
  start_systemd_service("/etc/systemd/system/kdnaconda.service")
  i=0
  while 1:
    i+=1
    command = 'echo "Hello les san ! - c le kdna du $(date +%Y%m%d-{})" >> /root/KDNA/logs.kdna'.format(i)  # tty0 au lieu du path vers logs pr afficher sur terminal
    subprocess.run(command, shell=True, check=True)
    time.sleep(10)


if __name__ == '__main__':
  main()
