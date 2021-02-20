#!/bin/sh
if [[ "$(tty)" == "/dev/tty1" ]]
  then
    echo "Welcome!"
    echo "Starting window manager..."
    sh $HOME/newm/main.sh
    echo "...closed"
fi
