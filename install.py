"""
Hyprmatrix lockscreen.
This script is intended for hyprland compositor.
(You may use the files in the script folder of this repository to adapt to your Wayland environment)
It will save two scripts and two config files on your swaylock directory. 
Make sure you have already installed:
    * swaylock-effects by mortie
    * kitty by kovidgoyal (You may use another terminal, but would need to edit files by hand)
    * cmatrix by abishekvashok OR unimatrix by will8211 (If you have both, the script will prioritize unimatrix)
"""

import os
from getpass import getuser
from subprocess import run


def get_user():
    print('Getting user... ', end="")
    user = getuser()
    if user == None:
        print('Fail!')
        user = input("User Name: ")
    print('OK')
    return user


def directory(usr:str):
    print('Getting directory... ', end="")
    folder = f'/home/{usr}/.config/swaylock'
    if not os.path.isdir(folder):
        print('Fail!')
        folder = input('Swaylock directory: ')
    print('OK')
    return folder

# The packages are checked simply by running the command with the version argument.
# If the return from the OS is zero, the command has run successfully, therefore the packages exist
def package_checking():
    print("Checking packages: ")
    hyprctl = run('hyprctl version', shell=True, capture_output=True)
    swaylock = run('swaylock -v', shell=True, capture_output=True)
    kitty = run('kitty -v', shell=True, capture_output=True)
    unimatrix = run('unimatrix -h', shell=True, capture_output=True)
    cmatrix = run('cmatrix -V', shell=True, capture_output=True)

    print("hyprland... ", end='')
    if hyprctl.returncode:
        print("Fail!")
        print("Couldn't run 'hyprctl version', is hyprland installed?")
        exit()
    print("OK")
    
    print("swaylock... ", end='')
    if swaylock.returncode:
        print("Fail!")
        print("Couldn't run 'swaylock -v', is swayland-effects installed?")
        exit()
    print("OK")

    print("kitty... ", end='')
    if kitty.returncode:
        print("Fail!")
        print("Couldn't run 'kitty -v', is kitty installed?")
        exit()
    print("OK")
    
    print("unimatrix... ", end='')
    if unimatrix.returncode:
        print("Fail!")
        print("cmatrix... ", end='')
        if cmatrix.returncode:
            print("Fail!")
            print("Couldn't run 'unimatrix -h' or 'cmatrix -V', is there a matrix simulator installed?")
            exit()
        print("OK")
        return 'cmatrix'
    else:
        print("OK")
        return 'unimatrix'

# The matrix command is created with the chosen color
# If the user has unimatrix, the background color can also be chosen
def matrix_script_gen(pkg:str):
    colors = {'1': "green", '2': "red", '3': "blue", '4': "white",
                    '5': "yellow", '6': "cyan", '7': "magenta", '8': "black"}
        
    print("""
Matrix COLOR?
    (1) Green   (2) Red   (3) Blue     (4) White
    (5) Yellow  (6) Cyan  (7) Magenta  (8) Black
""")

    op = input(">>> ")
    while op not in colors:
        op = input(">>> ")

    color = colors[op]
    
    if pkg == 'unimatrix':
        print("""
Unimatrix background color?
    (1) Green   (2) Red   (3) Blue     (4) White
    (5) Yellow  (6) Cyan  (7) Magenta  (8) Black
""")    
        op = input(">>> ")
        while op not in colors:
            op = input(">>> ")

        bg_color = colors[op]
        matrix = f"unimatrix -ai -c {color} -g {bg_color} -s 90 -l knnssaAg"
        
    elif pkg == 'cmatrix':
        matrix = f"cmatrix -abs -C {color}"
    
    script = f"""#!/bin/bash
sleep 0.3
{matrix}
"""
    return script

# swaylock-effects config with the background color set to transparent
#   and all the ring and circle colors are dark grey with a little transparency
# I seek this combination because it is way cooler when the letters drop past behind the clock
def sway_config_gen():
    swaylock_conf = """#
show-failed-attempts
clock
color=00000000
indicator
indicator-radius=100
indicator-thickness=10
line-color=00000077
ring-color=00000077
inside-color=00000077
key-hl-color=a09ab0
separator-color=00000000
text-color=a09ab0
text-caps-lock-color=""
line-ver-color=00000077
ring-ver-color=00000077
inside-ver-color=00000077
text-ver-color=a09ab0
ring-wrong-color=00000077
text-wrong-color=a09ab0
inside-wrong-color=00000077
inside-clear-color=00000077
text-clear-color=a09ab0
ring-clear-color=00000077
line-clear-color=00000077
line-wrong-color=00000077
bs-hl-color=a09ab0
grace=1
grace-no-mouse
grace-no-touch
datestr=%a, %B %e
timestr=%I:%M %p
fade-in=0.2
ignore-empty-password
"""
    return swaylock_conf

#kitty also has a background opacity, but this doesn't work on fullscreen if the
#  hyprland fullscreen is not already set. I find it redundent, but I'll just keep as comment
def kitty_conf_gen():
    kittyconf = """font_family      jetbrains mono nerd font
font_size        15
confirm_os_window_close 0
#background_opacity 0.8
"""
    return kittyconf


# The Main script.
# The kill command for terminate the matrix screens is invoked in
#   line with the swaylock, but to be called just after swaylock has closed
# It is kept in a kind of 'stand by' while the rest of the script run
# I check the number of monitors and then dispatch the matrix for each one
# The sleep command is to give time for hyprland to focus on each monitor before calling the matrix on them.
def lock_script_gen(path:str):
    k_path = os.path.join(path, 'kittyconf.conf')
    m_path = os.path.join(path, 'matrix.sh')

    lockcript = f"""#!/bin/bash
mtrx_command="kitty -c {k_path} --start-as=fullscreen {m_path}"

(swaylock && kill -9 $(pgrep -f "$mtrx_command")) &

#sleep 1 

checkpid=$(pgrep swaylock)
if ! [ -z $checkpid ]; then
	#swayidle &
	screens=$(hyprctl -j monitors | jq length)
	for (( i = 0; i < $screens; i++ ))
	do
		sleep 0.3
		hyprctl dispatch focusmonitor $i 
		eval $mtrx_command &
	done 
fi
"""
    return lockcript


#Presentation
print("""
Hyprmatrix lockscreen.
This script is intended for hyprland compositor.
(You may use the files in the script folder of this repository to adapt to your Wayland environment)
It will save two scripts and two config files on your swaylock directory. 
Make sure you have already installed:
    * swaylock-effects by mortie
    * kitty by kovidgoyal (You may use another terminal, but would need to edit files by hand)
    * cmatrix by abishekvashok OR unimatrix by will8211 (If you have both, the script will prioritize unimatrix)""")

i = input("Proceed? (Y/n) ")
if i not in ('Yy'):
    exit()

#Get the loged user, the right path for swaylock and checking if the packges are installed 
USER = get_user()
folder = directory(USER)
matrix_pkg = package_checking()

print("Generating Scripts... ", end="")
matrix_file_script = matrix_script_gen(matrix_pkg)
swaylock_config_file = sway_config_gen()
kittyconf_file = kitty_conf_gen()
lockscript_file_script = lock_script_gen(folder)
print("OK")

#Saving the scripts and config files generated on the swaylock directory
print(f"Saving files on directory {folder}")

print('matrix.sh... ', end='')
matrix_file_path = os.path.join(folder, 'matrix.sh')
with open(matrix_file_path, 'w') as mf:
    mf.write(matrix_file_script)
print('OK')

print('swayconfig... ', end='')
swaylock_config_path = os.path.join(folder, 'config')
with open(swaylock_config_path, 'w') as gf:
    gf.write(swaylock_config_file)
print('OK')

print('kittyconf.conf... ', end='')
kittyconf_file_path = os.path.join(folder, 'kittyconf.conf')
with open(kittyconf_file_path, 'w') as kf:
    kf.write(kittyconf_file)
print('OK')

print('lockscript.sh... ', end='')
lockscript_file_path = os.path.join(folder, 'lockscript.sh')
with open(lockscript_file_path, 'w') as lf:
    lf.write(lockscript_file_script)
print('OK')

#chmod because the scripts need permission for execution
print("exec chmod on the scrips... ", end='')
run(f'chmod +x {matrix_file_path}', shell=True)
run(f'chmod +x {lockscript_file_path}', shell=True)
print('OK')

# We need to add the fullscreen atribute on the hyprland config file
# To not add every time the script is runned, first, the line atribute is remove 
#   and then we add the attribute if the user wants
path = f'/home/{USER}/.config/hypr/hyprland.conf'

hyprconf_file = open(path)
for i, l in enumerate(hyprconf_file.readlines()):
    if 'fullscreen_opacity' in l:
        del_line = i+1
        run(f"sed -i '{del_line}d' {path}", shell=True) #Removed

print("Add background transparency? (It will affect other programs when fullscren)")
i = input(" (Y/n) >>>")
if i in ('Yy'):
    print('How much on a scale 9..1 (1 is almost transparent)')

    op = input(">>> ")
    while int(op) not in range(1, 10):
        op = input(">>> ")    

    hyprconf_file = open(path)
    for i, l in enumerate(hyprconf_file.readlines()):
        if 'decoration' in l:
            add_line = i + 2

    run(f"sed -i '{add_line}i fullscreen_opacity = 0.{op}' {path}", shell=True)#ADD

print('Done!')