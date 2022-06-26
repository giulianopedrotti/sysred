#!/bin/bash
echo "Enter on directory"
cd /opt/sysred
echo "Stopping sysred and nginx services"
systemctl stop nginx
systemctl stop sysred
echo "Update application sysred"
git pull
echo "Install Requirements"
source .venv/bin/activate
.venv/bin/pip install -r requirements.txt
echo "Starting nginx and sysred services"
systemctl start sysred
systemctl start nginx