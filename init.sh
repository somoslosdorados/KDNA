#!/bin/bash

# /!\ before launching this script, be sure to have 'main.py' and 'kdnad.service'

# This script follows the documentation steps.
# This script needs root rights.
# This script is to be launched on the server (or test VM).

# Creating the directory.
cd /root ; mkdir /root/kdna_service
mv /main.py /root/kdna_service/
mv /kdnad.service /etc/systemd/system
systemctl daemon-reload
systemctl enable kdnad.service
python3 /root/kdna_service/main.py


