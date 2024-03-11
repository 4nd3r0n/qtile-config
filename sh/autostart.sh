#!/bin/sh

feh --bg-fill $HOME/.local/share/backgrounds/anderon.png &
xsettingsd &
picom --no-vsync &
xinput --set-prop 10 'libinput Natural Scrolling Enabled' 1 &
syncthing -no-browser -no-restart -logflags=0 &