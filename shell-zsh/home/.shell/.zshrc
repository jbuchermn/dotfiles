source $HOME/.shell/.bashrc

# Plugins
plugins=(
    git
)

# ViM mode
bindkey -v
bindkey "^?" backward-delete-char

# tab-completion
autoload -U compinit
compinit -u

zstyle ':completion:*:descriptions' format '%U%B%d%b%u'
zstyle ':completion:*:warniings' format'%BNo matches for: %d%b'

# command-correction
setopt correctall

# Case insensitive matching is annoying
CASE_SENSITIVE="true"

# Do not share history
unsetopt share_history
SAVEHIST=1000
HISTFILE=~/.zsh_history


# git
alias gst='git status'
compdef _git gst=git-status

alias gl='git pull'
compdef _git gl=git-pull

alias gd='git diff'
compdef _git gd=git-diff

alias gp='git push'
compdef _git gp=git-push

alias gc='git commit -v'
compdef _git gc=git-commit

alias gco='git checkout'
compdef _git gco=git-checkout
alias gcm='git checkout master'

alias ga='git add'
compdef _git ga=git-add


# zsh-autosuggestions
source $HOME/.shell/zsh-autosuggestions/zsh-autosuggestions.zsh

# Starship prompt
eval "$(starship init zsh)"
