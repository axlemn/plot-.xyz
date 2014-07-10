#!/bin/bash

# Alexander Mun
# 06/17/14


case $# in
1)
    python init_timestamps.py $1
    ./watch_osx.sh 1 "python run_script.py $1"
    ;;
2)
    python init_timestamps.py $1 $2
    ./watch_osx.sh 1 "python run_script.py $1 $2"
    ;;
*)
    echo "Invalid number of arguments."
    exit
    ;;
esac
