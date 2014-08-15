# Alexander Mun
# 06/17/14

# Calls some terminal command on all files which need to be 
# updated

import subprocess
import shutil
import os
import time
import matplotlib_script as mpl
import threading
import re
from helper import *
import xyz_to_feff

FROM_CENTER = 5.0
METADATA_FILE = "temp.txt"
this_file_dir = os.path.dirname(os.path.realpath(__file__))

def update_file(f, *args):
    '''The main function.  This directs what is to be done to input 
    file f on update.  Should work on relative paths, but if that's not working,
    passing the absolute path won't hurt.

    As stated in the readme, here is a list of possible flags:
    -m will skip displaying output graphs.
    -e will use only paths from atoms nearby the center_of_mass 
    -n will avoid re-calculating paths in feff, i.e. assumes that the file 
        is already up-to-date and skips straight to calculating the average
        chi(k) and graphing
    '''

    def read_metadata(f, s):
        '''Looks in f's directory for a METADATA_FILE, and from it reads
        and returns the data corresponding to the string s.'''
        file_path = get_dirname(f, METADATA_FILE)
        temp = open(file_path, 'r')
        for l in temp:
            # Checks if the part of a string appearing 
            # before an = on a line is s, returns rest of line 
            if len(l) > 2 and "".join(l.split('=')) != "" and \
                ("".join(l.split())).split('=')[0].split()[0] == s:
                 return '='.join(l.split('=')[1:])

    def write_metadata(f, s, data):
        '''Looks in f's directory for a METADATA_FILE, and from it reads
        and returns the data corresponding to the string s.'''
        file_path = get_dirname(f, METADATA_FILE)
        already_exists = os.path.isfile(file_path)

        if already_exists:
            temp = open(file_path, 'r')
            search = None
            r = temp.readlines()
            temp.close()

            for (i,l) in enumerate(r):
                # Checks if the part of a string appearing 
                # before an = on a line is s, returns rest of line 
                if len(l) > 2 and "".join(l.split('=')) != "" and \
                    ("".join(l.split())).split('=')[0].split()[0] == s:
                     search = i

            if search != None:
                r.pop(search)

        temp = open(file_path, 'w')
        if already_exists:
            for l in r:
                temp.write(l)
            temp.write('\n')
        temp.write(s + "=" + data)
        temp.close()

    def calc_chik(f, run_index):
        '''Runs ifeffit_script.ps on dir with data from feff that has 
           the run_index atom in the center.  Zero indexed.'''
        print ['perl', 'ifeffit_script.ps', get_dirname(f, run_index)]
        subprocess.call(['perl', this_file_dir + '/' + 'ifeffit_script.ps', \
            get_dirname(f, run_index)])

    make_sure_path_exists(get_dirname(f))
    if '-n' not in args:
        ##############
        # Main loop:
        ##############

        # Gets center of mass to check edge effects
        atoms = scrape_xyz(f)
        if '-e' in args:
            center_of_mass = get_center_of_mass(atoms)
            write_metadata(f, "center_of_mass", str(center_of_mass))

        # Gets list of indices of Ta atoms
        central = xyz_to_feff.central_indices(atoms)

        # How many times to run?
        num_center_atoms = len(central)
        run_index = 0

        if '-e' in args:
            skipped = []
            not_skipped = []

        # To pay for speed in computing power, one could thread the following 
        # loop instead of doing each iteration consecutively
        for run_index in range(0, num_center_atoms):
            # Gets the nth atom of Ta before any shifting
            if '-e' in args:
                nth = atoms[central[run_index]]
                distsq = 0.0
                for i in range(1,4):
                    distsq += (center_of_mass[i-1]-float(nth[i]))**2
                if distsq > ((FROM_CENTER ** 2)-EPSILON):
                    print "Ta #" + str(run_index) + " at " +\
                            str(tuple(nth[1:3])) +\
                          " was too far. " + str((distsq)**(0.5))
                    skipped.append(central[run_index])
                    continue
                else:
                    not_skipped.append(run_index)

            # Making subdirectory to hold files for a fixed run index
            new_dir = get_dirname(f, run_index)
            make_sure_path_exists(new_dir)
    
            # xyz_to_feff.py called
            # Note1: .xyz file is assumed to use atomic symbols, and angstroms 
            # as coordinates 
            # Note2: xyz_to_feff is called every time.  It may seem redundant, 
            # but this allows slightly easier and more sensibly modular
            # pruning of the data to be done within xyz_to_feff.py
            # Note3: when run_index == 0, xyz_to_feff records num_center_atoms 
            # in temp.txt file.  No longer necessary.
            convert_xyz(f, run_index)
    
            # feff called
            run_feff(f, run_index)
            # ifeffit called on path files which feff just created
            calc_chik(f, run_index)

            run_index += 1

        if '-e' in args:
            write_metadata(f, "close_to_center_of_mass", str(not_skipped))
            write_metadata(f, "far_from_center_of_mass", str(skipped))
        ##################
    else: 
        atoms = scrape_xyz(f)
        center_of_mass = get_center_of_mass(atoms)
        central = xyz_to_feff.central_indices(atoms)
        num_center_atoms = len(central)

    ## Gathering chi(k) to push to matplotlib_script.py ##
    f_indices = range(0, num_center_atoms)
    if '-e' in args:
        if '-n'  in args:
            f_indices = read_metadata(f, "close_to_center_of_mass")
            f_indices = f_indices.replace('[', '')
            f_indices = f_indices.replace(']', '')
            f_indices = f_indices.replace(' ', '')
            f_indices = f_indices.replace('\n', '')
            f_indices = f_indices.split(',')
        else:
            f_indices = not_skipped
    f_list = []
    for i in f_indices:
        f_list.append( os.path.join(get_dirname(f, i), "ifeffit_out") )

    print "Averaging following %d chi(k) files: " % len(f_list)

    ### Graphing and plotting in matplotlib: ###

    if '-m' not in args:
        # Averaging must occur before graphs can open
        subprocess.call(['python', 
             this_file_dir + '/' + 'matplotlib_script.py',
             get_dirname(f), str(len(f_list))] + f_list + ['-a'])

        # Plotting averaged chi(k) and chi(r)
        # Opens subprocess via Popen to prevent matplotlib graphs from 
        # blocking loops in super-processes.  
        p = subprocess.Popen(['python', 
                            this_file_dir + '/' + 'matplotlib_script.py',
                            get_dirname(f), str(0), 
                            '-k', '-r'])

        # Would cause matplotlib plots to block terminal and monitoring 
        # loop until closed
        # p.wait()
        ############################################

    ### Cleanup ###
    clean(f, num_center_atoms)

def clean(f, num_center_atoms):
    ' Removes directories referring to Ta atoms which no longer exist. '
    for x in os.walk(get_dirname(f)):
        x_base = os.path.basename(x[0])
        if x_base.isdigit() and int(x_base) >= num_center_atoms:
            shutil.rmtree(x[0])

def convert_xyz(f, run_index):
    '''Creates a directory based on the run index (name determined via 
    get_dirname(f, run_index)), passes the run_index to xyz_to_feff.py, 
    and pipes the output into said directory.  '''

    new_dir = get_dirname(f, run_index)

    # Piping output of xyz_to_feff into subdirectory with the name 'feff.inp'
    f_name = new_dir + '/feff.inp'
    output_f = open(f_name, 'w')
    # 'Hi user, this is what I'm doing!'
    print "Converting xyz file...\n Writing output of "
    to_call = ['python', 
                this_file_dir + '/' + 'xyz_to_feff.py', 
                f, 
                str(run_index)]
    print ' '.join(to_call)
    print " to file " + f_name
    subprocess.call(to_call, stdout=output_f, stderr=subprocess.PIPE)
    output_f.close()

def run_feff(f, run_index):
    '''Calls feff after changing to the subdirectory obtained from 
    get_dirname(f, run_index).  Then changes directory back.  Assumes that 
    the directory exists, and that f_name is the correct feff input file.'''

    new_dir = get_dirname(f, run_index)
    f_name = new_dir + '/feff.inp'
    print "Calling feff, run index " + str(run_index) + "..."
    working_dir = os.getcwd()
    os.chdir(new_dir)
    subprocess.call(['feff6', f_name])
    os.chdir(working_dir)

if __name__ == '__main__':
    pass
