# Alexander Mun
# 06/17/14

# Creates a timestamp.txt file containing the timestamp info 
# for files in a given directory which fit a hard-coded regex.

# Note: that this will overwrite previous timestamp.txt files, 
# so be cautious if running this script in the same folder 
# for different directories!

import pickle
import os
import glob
import sys

default_ts_file = "timestamps.txt"

def store_stamps(new_stamps, ts_file):
    'Given a set of stamps, stores it in the timestamp file.'
    f = open(ts_file, 'w+')
    pickle.dump(new_stamps, f)
    f.close()

def open_records(ts_file):
    'Retrieves data from the timestamp file.'
    f = open(ts_file, 'r+')
    r = pickle.load(f)
    f.close()
    return r

def regex(dirname):
    'Gives regex stating what files to obtain from a given directory.'
    return dirname + '/*.xyz'

def get_stamps(dirname):
    'Gets set of stamps from directory.'
    temp = glob.glob(regex(dirname))
    s = set()
    for f in temp:
        s.add((f, os.path.getmtime(f)))
    return s

def stamps_to_files(stamps):
    'Extracts filenames from timestamps.'
    t = set()
    for s in stamps:
        t.add(s[0])
    return t

if __name__ == '__main__':    
#   Processes command line arguments
    args = sys.argv
    if len(args) not in [2,3]:
        print 'Usage error : takes in 2 or 3 arguments'
    temp_dir = args[1]
    if len(args) == 3:
        ts_file = args[2]
    else:
        ts_file = default_ts_file

    s = get_stamps(temp_dir)
    print s
    store_stamps(s, ts_file)
