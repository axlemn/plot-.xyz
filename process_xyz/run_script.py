# Alexander Mun
# 06/17/14

# Calls some terminal command on all files which need to be 
# updated, as specified

import subprocess
import shutil
import os
import errno
import time
import matplotlib_script as mpl
import threading

def make_sure_path_exists(path):
    '''Creates a directory if it did not previously exist.'''
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def get_dirname(f, subdir=""):
    '''Takes in a filename, and returns the pathname to use to hold
    all files relating to it.'''
    base = os.path.basename(f)

    if base == "":
        raise Exception("Tried to update an invalid path name!")

    d = os.path.dirname(os.path.abspath(f))
    return d +  "/" + base[:-4] + "/" + str(subdir)

def update_file(f):
    '''The main function.  This directs what is to be done to input 
    file f on update.  '''

    def read_num_center_atoms(f):
        '''Looks in f's directory for a temp.txt file, and from it reads
        and returns the number of center atoms.'''
        file_path = get_dirname(f, "temp.txt")
        temp = open(file_path, 'r')
        for l in temp:
            # Checks if the part of a string appearing 
            # before an = on a line is 'num_center_atoms'
            if l.split('=')[0].split()[0] == 'num_center_atoms':
                 num = int(l.split('=')[1].split()[0])
        return num

    def calc_chik(f, run_index):
        '''Runs ifeffit_script.ps on dir with data from feff that has 
           the run_index atom in the center.  Zero indexed.'''
        print ['perl', 'ifeffit_script.ps', get_dirname(f, run_index)]
        subprocess.call(['perl', 'ifeffit_script.ps', \
            get_dirname(f, run_index)])

    ##############
    # Main loop:
    ##############
    # Tracks how many times feff has been run:
    num_runs = 0
    # num_center_atoms is set within the loop, initializing 
    # arbitrarily so preconditions are met
    num_center_atoms = 1
    while num_runs < num_center_atoms:

        # Subdirectories made, xyz_to_feff called, feff called:
        # if num_runs == 0, records num_center_atoms in temp.txt file
        run_feff(f, num_runs)

        # If not done already, gets num_center_atoms via the temp.txt file
        if num_runs == 0:
            num_center_atoms = read_num_center_atoms(f)

        calc_chik(f, num_runs)

        num_runs += 1
    ##############

    ## Gathering and averaging chi(k) ##
    f_list = []
    unaveraged_chik = get_dirname(f, "paths")
    make_sure_path_exists(unaveraged_chiks)
    for i in range(0, num_center_atoms):
        f_list.append( get_dirname(f, i) + "/ifeffit_out", 

    ### Graphing and plotting in matplotlib: ###
    # Opens subprocess via Popen to prevent matplotlib graphs from blocking 
    # loops in superprocesses.  Graphs are created and plotted:
    subprocess.Popen(['python', 'matplotlib_script.py',
         get_dirname(f)] + f_list)

    ### Cleanup ###
    clean(f, num_center_atoms)

def clean(f, num_center_atoms):
    ' Removes directories referring to Ta atoms which no longer exist. '
    for x in os.walk(get_dirname(f)):
        x_base = os.path.basename(x[0])
        if x_base.isdigit() and int(x_base) >= num_center_atoms:
            shutil.rmtree(x[0])

def run_feff(f, run_index):
    '''Creates a directory based on the run index (name determined via 
    get_dirname(f, run_index)), passes the run_index to xyz_to_feff.py, 
    and pipes the output into said directory.  Moves to the directory, 
    runs feff, and moves back.'''

    # Making subdirectory for a fixed run index
    new_dir = get_dirname(f, run_index)
    make_sure_path_exists(new_dir)

    # Piping output of xyz_to_feff into subdirectory with the name 'feff.inp'
    f_name = new_dir + '/feff.inp'
    output_f = open(f_name, 'w')
    print "Converting xyz file...\n Writing output of "
    print "  python xyz_to_feff.py " + f + ' ' + str(run_index) 
    print " to file " + f_name
    subprocess.call(['python', 'xyz_to_feff.py', f, str(run_index)],\
        stdout=output_f, stderr = subprocess.PIPE)
    output_f.close()

    # Calls feff
    print "Calling feff, run index " + str(run_index) + "..."
    working_dir = os.getcwd()
    os.chdir(new_dir)
    subprocess.call(['feff6', f_name])
    os.chdir(working_dir)

if __name__ == '__main__':
    pass
