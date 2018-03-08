#!/bin/sh

missing=""

if [[ -z "$(command -v nvim)" ]]; then missing="$missing nvim"; fi
if [[ -z "$(command -v fzy)" ]]; then missing="$missing fzy"; fi
if [[ -z "$(command -v ag)" ]]; then missing="$missing the_silver_searcher"; fi
if [[ -z "$(command -v flake8)" ]]; then missing="$missing flake8"; fi
if [[ -z "$(command -v rc)" ]]; then missing="$missing rtags"; fi

if [[ "$missing" ]]; then
    echo "##########################################"
    echo ""
    echo "Please install:"
    for m in $missing; do
        echo "    $m"
    done
    echo ""
    echo "##########################################"
fi

