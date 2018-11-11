#!/bin/bash


ps -ef | grep "python3 app.py" | grep -v grep | awk '{ print $2 }' | xargs kill

sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 5000
source ~/venv/bin/activate
nohup python3 app.py &
