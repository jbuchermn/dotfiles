#!/bin/sh

if [ ! -d "$HOME/.shell/zsh-autosuggestions" ]; then
    echo "Installing zsh-autosuggestions..."
    git clone "https://github.com/zsh-users/zsh-autosuggestions" "$HOME/.shell/zsh-autosuggestions"
fi
