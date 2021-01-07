#!/usr/bin/env bash
# Run appropriate setup script

NODE_ID=$(geni-get client_id)

if [ $NODE_ID = "enb" ]; then
	/home/ses002/EasyLTE/srsLTE/start-enb.sh
elif [ $NODE_ID = "epc" ]; then
	/home/ses002/EasyLTE/srsLTE/start-epc.sh
else
	echo "No Setup Necessary"
fi