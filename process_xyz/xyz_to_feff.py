#!/usr/bin/env python
# Alexander Mun
# 07/02/2014

import periodic as pt
import sys
import re
import os.path
from helper import *

# How far can atoms be from the central atom before being disqualified?
ATOM_DIST_THRESHOLD=5

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

def central_indices(atoms, elt=central_elt):
    central_indices = []
    for (i,a) in enumerate(atoms):
        if a[0] == elt:
            central_indices.append(i)
    return central_indices

def shift_atoms(atoms, n, shift=True):
    '''Finds nth atom of type central_elt (the first is the zeroth), moves it to
    the front of the list, and shifts all atoms such that it 
    is at the center.'''
    center_index_counter = -1
    center_index = -1

    # Gets shift amount by from first element listed of type central_elt
    for (i,a) in enumerate(atoms):
        if a[0] == central_elt:
            center_index_counter += 1
            if center_index_counter == n:
                center_index = i

    if center_index == -1:
        raise Exception("No " + central_elt + " atom found to shift to center.")

    if shift == True:
        center = atoms.pop(center_index)
        atoms.insert(0, list(center))

        for (i,a) in enumerate(atoms): 
            a[1] = float(a[1]) - float(center[1])
            a[2] = float(a[2]) - float(center[2])
            a[3] = float(a[3]) - float(center[3])
    else:
        center = atoms[center_index]
        return center[:]

def prune_atom(atom):
    '''Given an 'atom' (a split line of data), returns whether or not 
    we want to ignore that atom during printing (and thus in feff, ifeffit, 
    etc).  Shifting will have finished before any atoms are pruned.'''
    if ((atom[1]**2 + atom[2]**2 + atom[3]**2) > \
                    (ATOM_DIST_THRESHOLD**2 + EPSILON)):
        return True
    return False

def output(f_name, n):
    """ 
    Prints the .feff conversion of a given xyz file to std.out.
    The nth Ta atom is shifted to the start of the file and to the center, 
    where n starts at 0.
    """

    atom_list = scrape_xyz(f_name)
    num_central = len(central_indices(atom_list))

    if n == 0:
        make_sure_path_exists(get_dirname(f_name))
        temp = open(get_dirname(f_name) + 'temp.txt', 'w')
        temp.write('num_center_atoms = ' + str(num_central))

    # n is an index
    if n >= num_central:
        return
    # Shifts first Ta atom to center and to the front
    shift_atoms(atom_list, n)

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
        if central_elt in elts and e == central_elt:
            if i == 0:
                sys.stdout.write('0')
            else:
                sys.stdout.write('1')
        sys.stdout.write('\n')

    sys.stdout.write('\n')

    print "ATOMS\n" \
          "* x         y         z       ipot"
    for (i, atom) in enumerate(atom_list):
        if prune_atom(atom):
            continue
        for j in range(1,4):
            # Six decimal places appears to be a standard, but 
            # may lose a very small amount of information.  
            atom[j] = format(atom[j], '.6f')
            sys.stdout.write(' '*(9-len(atom[j])))
            sys.stdout.write(atom[j])
            sys.stdout.write(' ')
        sys.stdout.write(' '*3)
        if i == 0:
            print '0'
        else: 
            print d[atom[0]]

    sys.stdout.write('\n')

    print('END')

if __name__ == '__main__':
    args = sys.argv
    if len(args) != 3:
        print 'Usage error.'
    f_name = args[1]
    n = int(args[2])
    # Formats a feff file with the nth Ta atom in the center
    output(f_name, n)
