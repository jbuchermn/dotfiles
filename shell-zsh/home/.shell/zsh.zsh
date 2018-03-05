source $SHELL_DIR/base.sh

# Plugins
plugins=(
    git
)


# ViM mode
bindkey -v
bindkey "^?" backward-delete-char


# zsh-autosuggestions
source $SHELL_DIR/zsh-autosuggestions/zsh-autosuggestions.zsh


# tab-completion
autoload -U compinit
compinit

zstyle ':completion:*:descriptions' format '%U%B%d%b%u'
zstyle ':completion:*:warniings' format'%BNo matches for: %d%b'


# command-correction
setopt correctall

# Case insensitive matching is annoying
CASE_SENSITIVE="true"

# oh-my-zsh
export ZSH=$SHELL_DIR/oh-my-zsh
ZSH_THEME="spaceship"
source $ZSH/oh-my-zsh.sh
