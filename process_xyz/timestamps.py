#!/usr/bin/env python
# Alexander Mun
# 06/17/14

# Creates a timestamp.txt file containing the timestamp info 
# for files in a given directory which fit a hard-coded regex.


import pickle
import os
import glob
import sys
from time import sleep
from run_script import update_file

def store_stamps(new_stamps, ts_file):
    'Given a set of stamps, stores it in the timestamp file.'
    f = open(ts_file, 'w+')
    pickle.dump(new_stamps, f)
    f.close()

def read_stamps(ts_file):
    'Retrieves data from the timestamp file.'
    f = open(ts_file, 'r+')
    r = pickle.load(f)
    f.close()
    return r

def get_stamps(dirname):
    'Gets set of stamps from directory.'
    temp = glob.glob(dirname + '/*.xyz')
    s = set()
    for f in temp:
        s.add((os.path.abspath(f), os.path.getmtime(f)))
    return s

def stamps_to_files(stamps):
    'Extracts filenames from timestamps.'
    t = set()
    for s in stamps:
        t.add(s[0])
    return t

def write_stamps(dirname, ts_file):
    'Processes command line arguments, gets and stores stamps'
    s = get_stamps(dirname)
    store_stamps(s, ts_file)
    return s

def find_modified(ts_file, dirname, new_stamps):
    '''Looks at old ts_file and compares with new timestamps.'''
    old_stamps = read_stamps(ts_file)
    changed_stamps = new_stamps - old_stamps
    return stamps_to_files(changed_stamps)

def main(dirname, ts_file):
    while True:
        # If the sleep interval is decreased be careful that 
        # the files are not modified faster than Python 2 can 
        # detect via getmtime: 
        # http://stackoverflow.com/questions/19351867/
        try:
            sleep(0.10)
            # New stamps are calculated here to avoid races b/w 
            # checks on timestamps and file updates
            new_stamps = get_stamps(dirname)
            files = find_modified(ts_file, dirname, new_stamps)
            if files != set(()):
                for f in files:
                    # All updated files are sent off to be processed!
                    update_file(f)
                    print f
                store_stamps(new_stamps, ts_file)
        except (KeyboardInterrupt, SystemExit):
            print "\n\nProgram ended by user input."
            exit(0)

if __name__ == '__main__':    
    args = sys.argv
    if len(args) not in [2,3]:
        print 'Usage: init_timestamps.py /dir/to/watch '\
            '[timestamp_file]'
        sys.exit(1)
    if len(args) == 2:
        args.append(os.path.abspath(args[1]) + '/timestamps.txt')
    print "Initial files found:"
    for f in write_stamps(*args[1:]):
        print f
    main(*args[1:])
