'''
Monitors our code & docs for changes

To get coverage:

    python -m coverage run -m unittest discover
    python -m coverage report -m
        Or: `python -m coverage html`

'''

import os
import sys
import subprocess
import datetime
import time
import run_script

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

def get_now():
    '''
    Get the current date and time as a string
    '''
    return datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")

def run_tests():
    '''
    Run unit tests with unittest.
    '''
    print 'Okay'

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
        print 'Modified'
        print event.src_path
        if getext(event.src_path) == '.xyz':
            print '.xyz -- MODIFIED'

    def on_created(self, event):
        '''
        If any file or folder is created
        '''
        print 'Creation'
        print event.src_path
        if getext(event.src_path) == '.xyz':
            # run_tests()
            run_script.update_file(event.src_path)
            print '.xyz CREATED'

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
