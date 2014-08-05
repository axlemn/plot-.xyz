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
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def update_file(f):
    '''The main function, which calls subprocesses and directs what will 
    be done to input file f on update.  Forms necessary metadata.'''

    print "Updating file " + f

    # Runs feff6, gets metadata, then runs ifeffit
    num_runs = 0
    # num_center_atoms is set within the loop, so setting up a 
    # for loop is not possible
    num_center_atoms = 1
    while num_runs < num_center_atoms:
        print "================"
        print "Running feff: run number " + str(num_runs)
        print "================"
        run_feff(f, num_runs)

        # If not done already, gets num_center_atoms from temp.txt file
        if num_runs == 0:
            file_path = get_dir_name(f, "temp.txt")
            temp = open(file_path, 'r')
            print 'Debug'
            for l in temp:
                # Checks first word before an = on a line 
                if l.split('=')[0].split()[0] == 'num_center_atoms':
                    num_center_atoms = int(l.split('=')[1].split()[0])

        # Calls ifeffit_script.ps
        run_ifeffit(f, num_runs)
        print num_runs

        num_runs += 1

    # Moves path files; NOTE THIS IS VERY REDUNDANT, TO FIX
    f_list = []
    path_files = get_dir_name(f, "paths")
    make_sure_path_exists(path_files)
    for i in range(0, num_center_atoms):
        shutil.copyfile( get_dir_name(f, i) + "/ifeffit_out", 
                       path_files + "/ifeffit_out" + str(i))
        f_list.append(path_files + "/ifeffit_out" + str(i))

 #  # Averages together .chi files from ifeffit
 #  mpl.avg(f_list, get_dir_name(f))

 #  # Displays avg
 #  mpl.display_avg(get_dir_name(f))

 #  # Displays ifeffit results via matplotlib_script.py
 #  mpl.main(f_list)

    subprocess.Popen(['python', 'matplotlib_script.py',
         get_dir_name(f)] + f_list)

    # Removes obsolete directories 
    for x in os.walk(get_dir_name(f)):
        x_base = os.path.basename(x[0])
        if x_base.isdigit() and int(x_base) >= num_center_atoms:
            shutil.rmtree(x[0])

def get_dir_name(f, *args):
    base = os.path.basename(f)

    if base == "":
        raise Exception("Tried to update an invalid path name!")

    d = os.path.dirname(os.path.abspath(f))

    if len(args) > 0:
        return d +  "/" + base[:-4] + "/" + str(args[0])
    return d +  "/" + base[:-4] + "/"

def run_feff(f, run_index):
    '''Creates directory, runs chain of commands on file and puts 
    output files in said directory'''

    # Making directory
    new_dir = get_dir_name(f, run_index)
    make_sure_path_exists(new_dir)

    # Piping output of xyz_to_feff
    f_name = new_dir + '/feff.inp'
    output_f = open(f_name, 'w')

    print "first converting xyz file..."
    print "calling",
    print ['python', 'xyz_to_feff.py', f, str(run_index)]
    print "to file " + f_name
    
    subprocess.call(['python', 'xyz_to_feff.py', f, str(run_index)],\
        stdout=output_f, stderr = subprocess.PIPE)
    output_f.close()

    working_dir = os.getcwd()
    os.chdir(new_dir)
    subprocess.call(['feff6', f_name])
    os.chdir(working_dir)

def run_ifeffit(f, run_index):
    '''Runs ifeffit_script.ps on dir with data from feff that has the run_index      atom in the center'''
    print ['perl', 'ifeffit_script.ps', get_dir_name(f, run_index)]
    subprocess.call(['perl', 'ifeffit_script.ps', get_dir_name(f, run_index)])

if __name__ == '__main__':
    pass
