#!/bin/python
import os
from getpass import getuser
from subprocess import run

# This script toggles the transparency of the fullscreen mode in Hyprland.
# It is intended to be used with a keyboard shortcut.

def get_user():
    print('Getting user... ', end="")
    user = getuser()
    if user == None:
        print('Fail!')
        user = input("User Name: ")
    print('OK')
    return user


USER = get_user()

path = f'/home/{USER}/.config/hypr/hyprland.conf'

hyprconf_file = open(path)
for i, l in enumerate(hyprconf_file.readlines()):
    if '#fullscreen_opacity' in l:
        run(f"sed -e '/#fullscreen_opacity/ s/^#//' -i {path}", shell=True)
        break
    elif 'fullscreen_opacity' in l:
        run(f"sed -e '/fullscreen_opacity/ s/^/#/' -i {path}", shell=True)
        break
