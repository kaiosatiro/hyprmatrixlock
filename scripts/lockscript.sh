#!/bin/bash
mtrx_command="kitty -c /home/<USER>/.config/swaylock/kittyconf.conf --start-as=fullscreen /home/<USER>/.config/swaylock/matrix.sh"

(swaylock && kill -9 $(pgrep -f $mtrx_command)) &

checkpid=$(pgrep swaylock)
if ! [ -z $checkpid ]; then
	#swayidle &
	screens=$(hyprctl -j monitors | jq length)
	for i in {0..$screens};
	do
		if [ $i -eq $screens ]; then
			break
		fi	
		sleep 0.3
		hyprctl dispatch focusmonitor $i 
		eval $mtrx_command &
	done 
fi
