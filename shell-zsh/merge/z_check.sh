#!/bin/bash

# Check if battery level can be read
if [[ -z "$(command -v pmset)" ]] && [[ -z "$(command -v upower)" ]]; then
    echo "#######################################"
    echo ""
    echo "WARNING! Could not find pmset or upower."
    echo ""
    echo "########################################"
fi

