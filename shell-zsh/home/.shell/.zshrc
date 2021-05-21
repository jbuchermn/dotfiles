source $HOME/.shell/.bashrc

# Plugins
plugins=(
    git
)


# ViM mode
bindkey -v
bindkey "^?" backward-delete-char


# zsh-autosuggestions
source $HOME/.shell/zsh-autosuggestions/zsh-autosuggestions.zsh


# tab-completion
autoload -U compinit
compinit -u

zstyle ':completion:*:descriptions' format '%U%B%d%b%u'
zstyle ':completion:*:warniings' format'%BNo matches for: %d%b'


# command-correction
setopt correctall

# Case insensitive matching is annoying
CASE_SENSITIVE="true"

# oh-my-zsh
ZSH_DISABLE_COMPFIX=true
export ZSH=$HOME/.shell/oh-my-zsh
ZSH_THEME="spaceship"
source $ZSH/oh-my-zsh.sh

# Do not share history
unsetopt share_history
