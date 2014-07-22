# Alexander Mun
# 06/17/14

# Calls some terminal command on all files which need to be 
# updated, as specified

from subprocess import call, PIPE
import os
import errno

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def update_file(f, index, length):
    '''Creates directory, runs chain of commands on file and puts 
    output files in said directory'''

    # Making directory
    d = os.path.dirname(os.path.abspath(f))
    base = os.path.basename(f)
    new_dir = d + str(index).zfill(length) + "/" + base[:-4]
    if base == "":
        raise Exception("Tried to update an invalid path name!")
    make_sure_path_exists(new_dir)
    
    # Piping output of xyz_to_feff
    f_name = new_dir + '/feff.inp'
    output_f = open(f_name, 'w')
    call(['python', 'xyz_to_feff.py', f],\
        stdout=output_f, stderr = PIPE)

    working_dir = os.getcwd()
    os.chdir(new_dir)
    call(['feff6', f_name])
    os.chdir(working_dir)

    print('Updated ' + f)
    output_f.close()

