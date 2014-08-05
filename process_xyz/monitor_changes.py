#!/usr/bin/env python
import os
import sys
import subprocess
import datetime
import time
import run_script

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

num_updates = 0

def get_now():
    '''
    Get the current date and time as a string
    '''
    return datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")

def getext(filename):
    '''
    Get the file extension.
    '''
    return os.path.splitext(filename)[-1].lower()

class ChangeHandler(PatternMatchingEventHandler):
    '''
    React to changes in Python and Rest files by
    running unit tests (Python) or building docs (.rst)
    '''
    ignore_directories = True

    def on_modified(self, event):
        '''
        If file is changed
        '''
        if getext(event.src_path) == '.xyz':
            print "============================================="
            print get_now()
            print "Change detected in file:",
            print os.path.basename(event.src_path)
            global num_updates
            num_updates += 1
            print "change number : " + str(num_updates)
            print "============================================="
            run_script.update_file(event.src_path)

    def on_created(self, event):
        '''
        If file is created
        '''
        # Subsumed within the on_modified triggers

def main():
    '''
    Called when run as main.
    Look for changes to code and doc files.
    '''

    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == '__main__':
    main()
