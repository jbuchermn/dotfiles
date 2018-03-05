#!/bin/sh

if [ -d "$HOME/.shell/spaceship-prompt" ]; then
    echo "Found spaceship-prompt. Skipping."
    exit 0
fi

echo "Installing spaceship-prompt..."
git clone "https://github.com/denysdovhan/spaceship-prompt.git" "$HOME/.shell/spaceship-prompt"

if  [ ! -d "$HOME/.shell/oh-my-zsh/custom/themes" ]; then
    mkdir -p "$HOME/.shell/oh-my-zsh/custom/themes"
fi

ln -s "$HOME/.shell/spaceship-prompt/spaceship.zsh-theme" "$HOME/.shell/oh-my-zsh/custom/themes/spaceship.zsh-theme"
