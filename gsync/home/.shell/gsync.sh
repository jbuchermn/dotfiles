canonical=$(cd -P -- "$(dirname -- "$0")" && printf '%s\n' "$(pwd -P)")
alias gsync="python3 $canonical/gsync.py"
