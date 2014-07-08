#!/bin/bash

# Alexander Mun
# 06/17/14

case $# in
1)
    python init_timestamps.py $1
    watch -n1 "python run_script.py $1"
    ;;
2)
    if [ ! -z $2 ]; then
            python init_timestamps.py $1 $2
            watch -n1 "python run_script.py $1 $2"
    fi
    ;;
*)
    echo "Invalid number of arguments."
    exit
    ;;
esac
