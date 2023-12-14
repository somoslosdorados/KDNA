
# DOC POC-6-TTC  

---

## 0. Préambule  
* Vous êtes connecté en tant que root. Votre dossier home est `/root`.  
Le service de ce POC va générer des logs.  

## I. Préparer l'environnement sur le serveur  
1. Créer le dossier `/root/kdna_service`  
2. Placer le fichier main.py à l'emplacement : `/root/kdna_service/main.py`  
3. Placer le fichier kdnad.service à l'emplacement `/etc/systemd/system`  

## II. Activer le service  
1. Lancer la commande `systemctl daemon-reload`  
2. Lancer la commande `systemctl enable kdnad.service`  
3. Lancer la commande `python3 /root/kdna_service/main.py`  
\
Des logs apparaissent alors dans `/root/kdna_service/logs.kdna`  

---

Si vous avez correctement configuré `pandoc`, vous pouvez utiliser la commande `pandoc doc.md -o doc.pdf -V geometry:margin=2.2cm`
Mes félicitations. Dieu nous garde.  

