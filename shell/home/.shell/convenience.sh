function md { 
    mkdir -p "$@" && cd "$1"; 
}

function fd {
    cd $(find ${1:-.} -type d | fzy)
}

function ld {
    ls $(find ${1:-.} | fzy)
}

function macho-gui {
    $HOME/.shell/macho-gui.sh
}
