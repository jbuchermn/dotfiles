# Note: Powerline fonts (used by nvim-dark and shell-zsh)

[Powerline](https://github.com/powerline/fonts)

# Note: Oceanic-Next theme for iTerm2

[OceanicNext](https://github.com/mhartington/oceanic-next-iterm)

# Note: True color support in Emacs

Version should be something like 26, 27, ... (25.3 did NOT work), start emacs with TERM=xterm-24bit emacs -nw

File install_terminfo_iterm2.sh

```bash
#!/bin/bash
tic -x -o ~/.terminfo install_terminfo_iterm2.src
```

File install_terminfo_iterm2.src

```bash
# Use colon separators.
xterm-24bit|xterm with 24-bit direct color mode,
   use=xterm-256color,
   setb24=\E[48:2:%p1%{65536}%/%d:%p1%{256}%/%{255}%&%d:%p1%{255}%&%dm,
   setf24=\E[38:2:%p1%{65536}%/%d:%p1%{256}%/%{255}%&%d:%p1%{255}%&%dm,
# Use semicolon separators.
xterm-24bits|xterm with 24-bit direct color mode,
   use=xterm-256color,
   setb24=\E[48;2;%p1%{65536}%/%d;%p1%{256}%/%{255}%&%d;%p1%{255}%&%dm,
   setf24=\E[38;2;%p1%{65536}%/%d;%p1%{256}%/%{255}%&%d;%p1%{255}%&%dm,
```

# Note: VBox Guest

Don't use guest iso provided by VirtualBox, follow instructions on Arch Wiki. For modesetting in X.Org:

```bash
xrandr --newmode "2560x1440x60.0"  348.50  2560 2752 3032 3504  1440 1441 1444 1500 -hsync +vsync
xrandr --addmode Virtual-1 "2560x1440x60.0"
xrandr --output Virtual-1 --mode "2560x1440x60.0"
```

where the first line can be found using 

```bash
cat /var/log/Xorg.0.log | grep modesetting
```

# Note: zsh remnant characters on tabcomplete

Make sure locale is set (`locale-gen`)

# Note: MBP suspend on Arch

https://wiki.archlinux.org/index.php/Power_management/Suspend_and_hibernate#Instantaneous_wakeups_from_suspend
