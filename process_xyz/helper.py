import os
import errno
import periodic

# Sets default names for files  
central_elt = "Ta"
default_chik = "chi.k"
default_chir = "chi.r"
EPSILON = 0.0000001
LOGFILE = "xyztofeff.log"

'''Contains many helper functions.  Ideally will not import libraries that are tempermental if imported multiple times.  Unfortunately periodic is very tempermental in threaded programs.  Sorry if you're trying to adapt this to watchdog, as this may cause issues.'''

def scrape_xyz(f_name):
#   Gets data from a file of format .xyz
    atom_lines = []
    f = open(f_name, 'r+')
    for (i,line) in enumerate(f):
#   if it's at least the 3rd line, and not blank:
        if line == "\n":
            continue
        if i > 1:
            atom_lines.append(line)

    atoms = []
    for l in atom_lines:
        atoms.append(l.split())
    if atoms == []:
        raise Exception(f_name + " has no data!")

    return atoms

def get_center_of_mass(atoms):
    mass = 0.0
    weighted_position = [0.0, 0.0, 0.0]
    for a in atoms:
        for i in range(1,4):
            a[i] = float(a[i])
        a_mass = periodic.element(a[0]).mass
        mass += a_mass
        weighted_position = [x + (a_mass * y) for x, y in \
            zip(weighted_position, a[1:4])]
    return [x/mass for x in weighted_position]

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
    return os.path.join(d, base[:-4], str(subdir))

if __name__ == '__main__':
    pass
