# Alexander Mun
# 06/17/14

# Calls some terminal command on all files which need to be 
# updated, as specified

from subprocess import call
from init_timestamps import *
from xyz_to_feff import title

def update_files(to_update):
    for f in to_update:
        fil = open(title(f) + '.inp', 'w')
        call(['python', 'xyz_to_feff.py', f], \
            stdout=fil)
        print('Updated ' + f)
        fil.close()

if __name__ == '__main__':
    dirname = sys.argv[1]
    if len(sys.argv) == 3:
        ts_file = sys.argv[2]
    else: 
        ts_file = default_ts_file

    curr_stamps = get_stamps(dirname)
    old_stamps  = open_records(ts_file)
    to_update = stamps_to_files(curr_stamps - old_stamps)

    update_files(to_update)
    store_stamps(curr_stamps, ts_file)
