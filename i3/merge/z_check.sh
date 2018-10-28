#!/bin/bash

# Check if backlight can be changed
if [[ -z "$(command -v xbacklight)" ]]; then
    echo "#######################################"
    echo ""
    echo "WARNING! Could not find xbacklight."
    echo ""
    echo "########################################"
fi

# Check if ALSA PulseAudio is installed
if [[ -z "$(command -v alsamixer)" ]] || [[ -z "$(command -v pactl)" ]]; then
    echo "#######################################"
    echo ""
    echo "WARNING! Could not find ALSA and PulseAudio."
    echo ""
    echo "########################################"
fi
