# Alexander Mun
# 07/02/2014

import periodic as pt
import sys
import re

# Note: have not yet enforced anything to do with central atom, nor 
# with having an atom at (0,0,0).
central = "Ta"
output = "d_feff.inp"

def title(f_name):
    if f_name[-4:] != ".xyz":
        raise Exception("`Not a .xyz file!")
    return "Test " + f_name[0:-4]

def scrape_xyz(f_name):

    atom_lines = []
    f = open(f_name, 'r+')
    for line in f:
#   if line fits regex:
        if re.match("[A-Z]", line):
            atom_lines.append(line)

#   Gets data from each of the lines
    atoms = []
    for l in atom_lines:
        atoms.append(l.split())
    return atoms

def elements(atoms):
    elements = []
    for a in atoms:
        if a[0] not in elements:
            elements.append(a[0])
    return elements

def dictionary_from_elts(elts):
    d = {}
    for (i,e) in enumerate(elts):
        d.update({e:i})
    return d

if __name__ == '__main__':
    args = sys.argv
    if len(args) != 2:
        print 'Usage error.'
    f_name = args[1]

    atom_list = scrape_xyz(f_name)

    print "TITLE %s\n" % title(f_name)
    print "CONTROL 1 1 1 1 1 1\n" \
          "PRINT   0 0 0 0 0 0\n"
    print "POTENTIALS\n" \
          "* potential-index   z   tag"

    elts = elements(atom_list)
    d = dictionary_from_elts(elts)

    for (i,e) in enumerate(elts): 
# Using an alternate printing method to get around python spacing issues
        sys.stdout.write(' '*9)
        sys.stdout.write(str(i))
        sys.stdout.write(' '*(11-len(str(i))))
        atomic_num = pt.element(e).atomic
        sys.stdout.write(str(atomic_num))
        sys.stdout.write(' '*(4-len(str(atomic_num))))
        sys.stdout.write(e)
        sys.stdout.write('\n')

    sys.stdout.write('\n')

    print "ATOMS\n" \
          "* x        y        z       ipot"
    for atom in atom_list:
        for i in range(1,4):
            sys.stdout.write(' '*(9-len(atom[i])))
            sys.stdout.write(atom[i])
        sys.stdout.write(' '*3)
        print d[atom[0]]

    sys.stdout.write('\n')

    print('END')
            
    

