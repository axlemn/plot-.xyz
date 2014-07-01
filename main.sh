#!/bin/bash

# Alexander Mun
# 06/17/14

python init_timestamps.py $1

watch -n1 "python run_script.py $1"
