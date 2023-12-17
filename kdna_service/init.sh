#!/bin/bash

# /!\ before launching this script, be sure to have 'main.py' and 'kdnad.service' at '/' on your server.
# Make this script executable as root. This can be done using chmod u+x init.sh as root.

# This script follows the documentation steps as described in doc.md. It is recommended to read doc.md first.
# This script needs root rights.
# This script is to be launched on the server (or test VM).

# Setting up  the filesystem for the service.
cd /root ; mkdir /root/kdna_service
mv /main.py /root/kdna_service/
mv /kdnad.service /etc/systemd/system

# Enabling and starting the daemon.
systemctl daemon-reload
systemctl enable kdnad.service
systemctl start kdnad.service

