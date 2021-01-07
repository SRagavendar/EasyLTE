#!/bin/bash

set -ux
tmux new-sessions -d -s enb
tmus send-keys 'sudo srsenb /home/ses002/EasyLTE/config/srsenb' C-m
tmux split-window -v
tmux select-layout even-vertical
tmux attach-session -d -t enb