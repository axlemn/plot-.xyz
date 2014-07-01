# Alexander Mun
# 06/17/14

from subprocess import call
from init_timestamps import *

cmd = 'cat'

def update_files(to_update):
    for f in to_update:
        call([cmd, f])
        print('Updated ' + f)

if __name__ == '__main__':
    dirname = sys.argv[1]

    curr_stamps = get_stamps(dirname)
    old_stamps  = open_records(default_ts_file)
    to_update = stamps_to_files(curr_stamps - old_stamps)

    update_files(to_update)
    store_stamps(curr_stamps, default_ts_file)
    
