#!/bin/bash
mtrx_command="kitty -c /home/<USER>/.config/swaylock/kittyconf.conf --start-as=fullscreen /home/<USER>/.config/swaylock/matrix.sh"

# fulltransparency_off="sed -e '/fullscreen_opacity/ s/^/#/' -i /home/<USER>/.config/hypr/hyprland.conf"
# fulltransparency_on="sed -e '/#fullscreen_opacity/ s/^#//' -i -i /home/<USER>/.config/hypr/hyprland.conf"


# This next command will run swaylock and the command to kill the matrix process, but only after
# 	swaylock has been closed (the unlocking), thanks for the '&&' operator.
# Using the parenthesis, these two commands will run in a sub-shell, 
#      while the rest of the script will continue to run, thanks to the '&' operator.
# The 'kill -9' will kill every process that was started with the command in the $mtrx_command variable.
(swaylock && kill -9 $(pgrep -f "$mtrx_command")) &

# (swaylock && kill -9 $(pgrep -f "$mtrx_command") && $fulltransparency_off) &


# eval $fulltransparency_on
#sleep 1 

checkpid=$(pgrep swaylock) # Check if swaylock is running
if ! [ -z $checkpid ]; then
	#swayidle &
	screens=$(hyprctl -j monitors | jq length) # Get the number of screens
	for (( i = -1; i < $screens; i++ ))
	do
		sleep 0.3
		hyprctl dispatch focusmonitor $i 
		eval $mtrx_command & # Run the matrix script
	done 
fi
