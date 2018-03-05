#!/bin/sh
if [ -d "$HOME/.shell/z" ]; then
    echo "Found z. Skipping"
    exit 0
fi

echo "Installing z..."
git clone "https://www.github.com/rupa/z" "$HOME/.shell/z"
