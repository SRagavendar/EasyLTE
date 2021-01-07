#!/bin/bash

set -ux
tmux new-session -d -s enb
tmux send-keys 'sudo srsenb /home/ses002/EasyLTE/config/srsenb/enb.conf' C-m
sleep 1.0
tmux split-window -v
tmux select-layout even-vertical
tmux attach-session -d -t enb