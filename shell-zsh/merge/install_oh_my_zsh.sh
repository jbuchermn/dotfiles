#!/bin/sh

# oh-my-zsh
if [ ! -d "$HOME/.shell/oh-my-zsh" ]; then
    if [ ! -d "$HOME/.shell" ]; then
        mkdir -p "$HOME/.shell"
    fi

    echo "Installing oh-my-zsh..."
    git clone --depth=1 "https://github.com/robbyrussell/oh-my-zsh.git" "$HOME/.shell/oh-my-zsh"

else
    echo "Found oh-my zsh. Skipping"
fi

# spaceship-prompt
if [ ! -d "$HOME/.shell/spaceship-prompt" ]; then
    echo "Installing spaceship-prompt..."
    git clone "https://github.com/denysdovhan/spaceship-prompt.git" "$HOME/.shell/spaceship-prompt"

    if  [ ! -d "$HOME/.shell/oh-my-zsh/custom/themes" ]; then
        mkdir -p "$HOME/.shell/oh-my-zsh/custom/themes"
    fi

    ln -s "$HOME/.shell/spaceship-prompt/spaceship.zsh-theme" "$HOME/.shell/oh-my-zsh/custom/themes/spaceship.zsh-theme"
fi
