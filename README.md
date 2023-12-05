<h1 align="center"> matrix lockscreen theme for linux </h1>

<h3 align="center"> This script is intended for hyprland compositor. </h3>
<h3 align="center"> MIT license </h3>

<h2>Make sure you have already installed:</h2>
<ul>
  <li> [swaylock-effects](https://github.com/mortie/swaylock-effects) by mortie </li>
  <li> [kitty](https://github.com/kovidgoyal/kitty) by kovidgoyal (You may use another terminal, but would need to edit files by hand) </li>
  <li> [cmatrix](https://github.com/abishekvashok/cmatrix) by abishekvashok OR [unimatrix](https://github.com/will8211/unimatrix) by will8211 (If you have both, the script will prioritize unimatrix) </li>
</ul>

Have these packages installed. Run the scripts, and choose the colors and transparency. 
Then, add on hyprland config file the bind command with the script:
```
bind = $mainMod, L, exec, /home/<USER>/.config/swaylock/lockscript.sh
```
After that, you can use the script to quickly change colors.

This script is intended for hyprland compositor, But we may use the script to adapt to your Wayland environment.

<h2>Video</h2>
https://github.com/kaiosatiro/hyprmatrixlock/assets/87156189/16280ab1-d805-4ac7-8c5e-d8e32e0c8604
