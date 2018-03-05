#!/bin/sh

if [ -d "$HOME/.shell/oh-my-zsh" ]; then
    echo "Found oh-my-zsh. Skipping."
    exit 0
fi

echo "Installing oh-my-zsh..."
git clone --depth=1 "https://github.com/robbyrussell/oh-my-zsh.git" "$HOME/.shell/oh-my-zsh"


