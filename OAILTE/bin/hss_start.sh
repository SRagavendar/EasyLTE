#!/bin/bash

OAIETCDIR="/home/ses002/EasyLTE/OAILTE/etc"

cd /home/ses002/oai/openair-cn/scripts

# Kill-off running function
./run_hss -k >/dev/null 2>&1
sleep 1

# Startup function
screen -c $OAIETCDIR/hss.screenrc -L -S hss -d -m -h 10000 /bin/bash -c "./run_hss"

# Some cleanup
screen -wipe >/dev/null 2>&1

exit 0