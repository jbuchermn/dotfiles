#!/bin/sh
if [ -d "$HOME/.cache/dein" ]; then
    echo "~/.cache/dein is present. Skipping."
    exit 0
fi

echo "Installing dein.vim..."
curl -s "https://raw.githubusercontent.com/Shougo/dein.vim/master/bin/installer.sh" | sh /dev/stdin "$HOME/.cache/dein"
