#!/bin/bash

cd /home/ses002/oai/openair-cn/scripts/

# Kill off running function
./run_mme -k
sleep 1

# Some cleanup
screen -wipe >/dev/null 2>&1

exit 0