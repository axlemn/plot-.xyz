#!/usr/bin/env python
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

    # This never causes a crash, for some reason
    if atoms == []:
        raise Exception(f_name + " has no data!")

    return atoms

def elements(atoms):
#   Lists the elements in a list of atoms.
    elements = []
    for (i,a) in enumerate(atoms):
        if i == 0: continue;
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

def find_central(atoms):
    central_list = []

    # Gets shift amount by from first element listed of type central_elt
    for (i,a) in enumerate(atoms):
        if a[0] == central_elt:
            central_list.append(i)

    if central_list == []:
        raise Exception("No " + central_elt + " atom found to shift to center.")

    return central_list

def shift_atoms(atoms, center_index):
    '''Finds nth atom of type central_elt, and shifts all atoms such that it 
    is at the center.'''

    center = atoms[center_index]

    #   Will cause rounding issue if .xyz changes the standard to be more 
    #   than 5 decimal places.  
    for (i,a) in enumerate(atoms): 
        a[1] = float(a[1]) - float(center[1])
        a[2] = float(a[2]) - float(center[2])
        a[3] = float(a[3]) - float(center[3])
        for i in range(1,4):
            a[i] = format(a[i], '.5f') 

def output(atom_list, center_index):
    """ 
    Prints the .feff conversion of a given xyz file to std.out.
    The first atom is assumed to be the central atom.
    """

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

        # Fixes central element to potential 0
        if central_elt in elts and e == central_elt:
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
        if i == center_index:
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
    atom_list = scrape_xyz(f_name)

    potential_centers = (find_central(atom_list))
    # Shifts each Ta atom to center in turn
    for i in range(len(potential_centers)):
        shift_atoms(atom_list, potential_centers[i])
        output(atom_list, potential_centers[i])
