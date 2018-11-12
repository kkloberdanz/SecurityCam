#!/bin/bash


ps -ef | grep "gunicorn" | grep -v grep | awk '{ print $2 }' | xargs kill

sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 5000
source /home/pi/venv/bin/activate
cd /home/pi/SecurityCam/
nohup gunicorn --workers 4 --bind 192.168.0.103:5000 app:app &
