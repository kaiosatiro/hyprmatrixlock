#This Scrip will ...
import os
from subprocess import run

matrix_file_script = """#!/bin/bash
sleep 0.3
unimatrix -ai -c blue -s 90 -l knnssaAg
"""

lockscript_file_script = """#!/bin/bash
mtrx_command="kitty -c /home/{user}/.config/swaylock/kittyconf.conf --start-as=fullscreen /home/{user}/.config/swaylock/matrix.sh"

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
"""

kittyconf_file = """font_family      jetbrains mono nerd font
font_size        15
#Close the terminal without confirmation
confirm_os_window_close 0
background_opacity 0.95
"""

swaylock_config_file = """#daemonize
show-failed-attempts
clock
color=00000000
indicator
indicator-radius=100
indicator-thickness=10
line-color=111111
ring-color=111111
inside-color=111111
key-hl-color=a09ab0
separator-color=00000000
text-color=a09ab0
text-caps-lock-color=""
line-ver-color=111111
ring-ver-color=111111
inside-ver-color=111111
text-ver-color=a09ab0
ring-wrong-color=111111
text-wrong-color=a09ab0
inside-wrong-color=111111
inside-clear-color=111111
text-clear-color=a09ab0
ring-clear-color=111111
line-clear-color=111111
line-wrong-color=111111
bs-hl-color=a09ab0
grace=2
grace-no-mouse
grace-no-touch
datestr=%a, %B %e
timestr=%I:%M %p
fade-in=0.2
ignore-empty-password
"""

user = os.getlogin()
#getpass.getuser()

folder = f'/home/{user}/.config/swaylock/test'

os.path.isdir(folder)

cmatrix = run('cmatrix -V', shell=True, capture_output=True)
swaylock = run('swaylock -V', shell=True, capture_output=True)
unimatrix = run('unimatrix -h', shell=True, capture_output=True)
hyprctl = run('hyprctl version', shell=True, capture_output=True)
kitty = run('kitty -v', shell=True, capture_output=True)


matrix_file_path = os.path.join(folder, 'matrix.sh')
with open(matrix_file_path, 'w') as mf:
    mf.write(matrix_file_script)

lockscript_file_path = os.path.join(folder, 'lockscript.sh')
with open(lockscript_file_path, 'w') as lf:
    lf.write(lockscript_file_script)

kittyconf_file = os.path.join(folder, 'kittyconf.conf')
with open(kittyconf_file, 'w') as kf:
    kf.write(kittyconf_file)

swaylock_config_path = os.path.join(folder, 'config.sh')
with open(swaylock_config_path, 'w') as gf:
    gf.write(swaylock_config_file)

run(f'chmod +x {matrix_file_path}', shell=True)
run(f'chmod +x {lockscript_file_path}', shell=True)
