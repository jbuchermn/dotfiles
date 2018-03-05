#!/bin/sh

if [-d "$HOME/.shell/zsh-autosuggestions" ]; then
    echo "Found zsh-autosuggestions. Skipping."
    exit 0
fi

echo "Installing zsh-autosuggestions..."
git clone "https://github.com/zsh-users/zsh-autosuggestions" "$HOME/.shell/zsh-autosuggestions"
