#!/bin/bash

# Alexander Mun
# 06/17/14

# If there is a nonempty second argument:
if [ ! -z $2 ]; then
        python init_timestamps.py $1 $2
        watch -n1 "python run_script.py $1 $2"
fi

# Otherwise:
python init_timestamps.py $1
watch -n1 "python run_script.py $1"
