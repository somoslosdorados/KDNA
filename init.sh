#!/bin/bash

cd /root ; mkdir /root/kdna_service
mv /main.py /root/kdna_service
mv /kdnad.service /etc/systemd/system

systemctl daemon-reload
systemctl enable kdnad.service
systemctl start kdnad.service