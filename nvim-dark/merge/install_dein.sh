#!/bin/sh
if [ -d "$HOME/.dein" ]; then
    echo "~/.dein is present. Skipping."
    exit 0
fi

echo "Installing dein.vim..."
curl -s "https://raw.githubusercontent.com/Shougo/dein.vim/master/bin/installer.sh" | sh /dev/stdin "$HOME/.dein"
