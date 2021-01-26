#!/bin/sh
if [[ "$(tty)" == "/dev/tty1" ]]
  then
    echo "Welcome!"
    echo "Starting window manager..."
    sh $HOME/pywm/main/main.sh
    echo "...closed"
fi
