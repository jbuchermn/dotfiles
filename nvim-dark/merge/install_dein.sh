#!/bin/sh
if [ -d "$HOME/.dein" ]; then
    echo "~/.dein is present. Skipping."
    exit 0
fi

curl https://raw.githubusercontent.com/Shougo/dein.vim/master/bin/installer.sh > /tmp/installer.sh
sh /tmp/installer.sh "$HOME/.dein"
