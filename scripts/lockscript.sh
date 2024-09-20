#!/bin/bash
mtrx_command="kitty -c /home/css/.config/swaylock/kittyconf.conf --start-as=fullscreen /home/css/.config/swaylock/matrix.sh"

(swaylock && kill -9 $(pgrep -f "$mtrx_command")) &

#sleep 1 

checkpid=$(pgrep swaylock)
if ! [ -z $checkpid ]; then
	#swayidle &
	screens=$(hyprctl -j monitors | jq length)
	for (( i = -1; i < $screens; i++ ))
	do
		sleep 0.3
		hyprctl dispatch focusmonitor $i 
		eval $mtrx_command &
	done 
fi
