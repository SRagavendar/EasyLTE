#!/bin/bash

OAIETCDIR="/home/ses002/EasyLTE/OAILTE/etc"

cd /home/ses002/oai/openair-cn/scripts

# Kill off running function
./run_spgw -k >/dev/null 2>&1
sleep 1

# Startup function
screen -c $OAIETCDIR/spgw.screenrc -L -S spgw -d -m -h 10000 /bin/bash -c "./run_spgw"

# Some cleanup
screen -wipe >/dev/null 2>&1

exit 0