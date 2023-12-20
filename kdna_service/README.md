
# DOC POC-6-TTC  

This POC is about a service which will generate logs as a demonstration.  
Every step in this documentation is followed by the `init.sh` script.  

---

## 0. Preamble  
* You are connected as root. Your home folder is `/root`. 

## I. Setting up the directories on the server  
1. Create the directory `/root/kdna_service`.  
2. Place the `main.py` file in the location: `/root/kdna_service/main.py`.  
3. Place the `kdnad.service` file in the location: `/etc/systemd/system/`.  

## II. Activate the service  
1. Run the command: `systemctl daemon-reload`.  
2. Run the command: `systemctl enable kdnad.service`.  
3. Run the command: `python3 start kdnad.service`.  

Logs will now appear periodically in `/root/kdna_service/logs.kdna`.  

---

If you have configured `pandoc` correctly, you can use the command `pandoc doc.md -o doc.pdf -V geometry:margin=2.2cm` to produce a pdf from this documentation.  
Congratulations.  

