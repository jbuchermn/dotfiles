#!/bin/sh
awk -v term_cols="${width:-$(tput cols || echo 80)}" 'BEGIN{
    s="/\\";
    for(colnum=0; colnum<term_cols; colnum++){
        r = 255-(colnum*255/term_cols);
        g = (colnum*510/term_cols);
        b = (colnum*255/term_cols);
        if(g>255) g  = 510 - g;
        printf "\033[48;2;%d;%d;%dm", r,g,b;
        printf "\033[38;2;%d;%d;%dm", 255-r,255-g,255-b;
        printf "%s\033[0m", substr(s, colnum%2+1,1);
    }
}'

source oceanic_next.sh

function hex_to_escape (){
    local hex=$1
    local r=${hex:1:2}
    local g=${hex:3:2}
    local b=${hex:5:2}

    r=$(echo $r | tr 'a-z' 'A-Z')
    g=$(echo $g | tr 'a-z' 'A-Z')
    b=$(echo $b | tr 'a-z' 'A-Z')

    r=$(echo "ibase=16; $r" | bc)
    g=$(echo "ibase=16; $g" | bc)
    b=$(echo "ibase=16; $b" | bc)
    
    printf "\033[48;2;%d;%d;%dm" $r $g $b
}


hex_to_escape $COLOR_SCHEME_01
printf "    "
printf "\033[0m"
printf " Color 01"
printf "\n"

hex_to_escape $COLOR_SCHEME_02
printf "    "
printf "\033[0m"
printf " Color 02" 
printf "\n"

hex_to_escape $COLOR_SCHEME_03
printf "    "
printf "\033[0m"
printf " Color 03" 
printf "\n"

hex_to_escape $COLOR_SCHEME_04
printf "    "
printf "\033[0m"
printf " Color 04" 
printf "\n"

hex_to_escape $COLOR_SCHEME_05
printf "    "
printf "\033[0m"
printf " Color 05" 
printf "\n"

hex_to_escape $COLOR_SCHEME_06
printf "    "
printf "\033[0m"
printf " Color 06" 
printf "\n"

hex_to_escape $COLOR_SCHEME_07
printf "    "
printf "\033[0m"
printf " Color 07" 
printf "\n"

hex_to_escape $COLOR_SCHEME_08
printf "    "
printf "\033[0m"
printf " Color 08" 
printf "\n"

hex_to_escape $COLOR_SCHEME_09
printf "    "
printf "\033[0m"
printf " Color 09" 
printf "\n"

hex_to_escape $COLOR_SCHEME_0A
printf "    "
printf "\033[0m"
printf " Color 0A" 
printf "\n"

hex_to_escape $COLOR_SCHEME_0B
printf "    "
printf "\033[0m"
printf " Color 0B" 
printf "\n"

hex_to_escape $COLOR_SCHEME_0C
printf "    "
printf "\033[0m"
printf " Color 0C" 
printf "\n"

hex_to_escape $COLOR_SCHEME_0D
printf "    "
printf "\033[0m"
printf " Color 0D" 
printf "\n"

hex_to_escape $COLOR_SCHEME_0E
printf "    "
printf "\033[0m"
printf " Color 0E" 
printf "\n"

hex_to_escape $COLOR_SCHEME_0F
printf "    "
printf "\033[0m"
printf " Color 0F" 
printf "\n"

hex_to_escape $COLOR_SCHEME_10
printf "    "
printf "\033[0m"
printf " Color 10" 
printf "\n"
