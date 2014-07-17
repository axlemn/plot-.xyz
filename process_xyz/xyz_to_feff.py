# Alexander Mun
# 07/02/2014

import periodic as pt
import sys
import re
import os.path

central_elt = "Ta"

def scrape_xyz(f_name):
#   Gets data from a file of format .xyz
    atom_lines = []
    f = open(f_name, 'r+')
    for (i,line) in enumerate(f):
#   if it's at least the 3rd line:
        if i > 1:
            atom_lines.append(line)

    atoms = []
    for l in atom_lines:
        atoms.append(l.split())
    return atoms

def elements(atoms):
#   Lists the elements in a list of atoms.
    elements = []
    for a in atoms:
        if a[0] not in elements:
            elements.append(a[0])
    return elements

def dictionary_from_elts(elts):
#   Dictionary giving potential-index given an element
    d = {}
    # Ensures that potential 0 is reserved for central atom
    for (i,e) in enumerate(['CENTER'] + elts):
        d.update({e:i})
    return d

def shift_atoms(atoms):
    '''Finds first atom of type central_elt, moves it to
    the front of the list, and shifts all atoms such that it 
    is at the center.'''
    center_index = -1

    # Gets shift amount by from first element listed of type central_elt
    for (i,a) in enumerate(atoms):
        if center_index == -1 and a[0] == central_elt:
            center_index = i

    if center_index == -1:
        raise Exception("No " + central_elt + " atom found to shift to center.")

    center = atoms.pop(center_index)
    atoms.insert(0, list(center))

    #   Will cause rounding issue if .xyz changes the standard to be more 
    #   than 5 decimal places.  
    for (i,a) in enumerate(atoms): 
        a[1] = float(a[1]) - float(center[1])
        a[2] = float(a[2]) - float(center[2])
        a[3] = float(a[3]) - float(center[3])
        for i in range(1,4):
            a[i] = format(a[i], '.5f') 


def output(f_name):
    """ 
    Prints the .feff conversion of a given xyz file to std.out.
    """

    atom_list = scrape_xyz(f_name)
    # Shifts first Ta atom to center and to the front
    shift_atoms(atom_list)

    # Gets elements of non-central atoms 
    elts = elements(atom_list)
    # And assigns non-central atoms positive potential
    d = dictionary_from_elts(elts)

    print "TITLE %s\n" % os.path.basename(f_name)[:-4]
    print "CONTROL 1 1 1 1 1 1\n" \
          "PRINT   0 0 0 0 0 0\n"
    print "POTENTIALS\n" \
          "* potential-index   z   tag"

    for (i,e) in enumerate([central_elt] + elts): 
        atomic_num = pt.element(e).atomic

        sys.stdout.write(' '*9)
        sys.stdout.write(str(i))
        sys.stdout.write(' '*(11-len(str(i))))
        sys.stdout.write(str(atomic_num))
        sys.stdout.write(' '*(4-len(str(atomic_num))))
        sys.stdout.write(e)
        if e == central_elt:
            if i == 0:
                sys.stdout.write('0')
            else:
                sys.stdout.write('1')
        sys.stdout.write('\n')

    sys.stdout.write('\n')

    print "ATOMS\n" \
          "* x        y        z       ipot"
    for (i, atom) in enumerate(atom_list):
        for j in range(1,4):
            sys.stdout.write(' '*(9-len(atom[j])))
            sys.stdout.write(atom[j])
        sys.stdout.write(' '*3)
        if i == 0:
            print '0'
        else: 
            print d[atom[0]]

    sys.stdout.write('\n')

    print('END')
            
if __name__ == '__main__':
    args = sys.argv
    if len(args) != 2:
        print 'Usage error.'
    f_name = args[1]
    output(f_name)
