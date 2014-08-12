import matplotlib.pyplot as plt
import sys
import subprocess
import os
from helper import *

default_chik = "chi.k"
default_chik_sq = "chiksq.k"
default_chik_cubed = "chikcubed.k"
default_chir = "chi.r"

def display_avg(dirname):
    make_window(dirname + '/' + default_chik)

def avg(f_list, dirname):
    count = len(f_list)
    d = {}
    d_init_flag = True
    for f_name in f_list:
        f = open(f_name, 'r')
        for line in f:
            s = line.split()
            if line[0] == "#":
                continue
            if d_init_flag == True:
                d[float(s[0])] = float(s[1])
            else:
                d[float(s[0])] += float(s[1])
        if d_init_flag == True:
            d_init_flag = False

        f.close()

    for key in d:
        d[key] /= count

    # Sort Keys, so matplotlib acts more sensible
    sorted_keys = []
    for key in d: 
        sorted_keys.append(key)
    sorted_keys.sort()
    for (i, key) in enumerate(sorted_keys):
        sorted_keys[i] = (key, d[key])

    f = open(dirname + '/' + default_chik, 'w')
    write_data(f, sorted_keys)

def read_data(f_name):
    data = []
    f = open(f_name, 'r+')
    for line in f:
        if line[0] == '#':
            continue
        data.append(line.split())
    f.close()
    return data

def write_data(f, sorted_keys):
    '''Writes sorted_keys for matplotlib to read to file object f.'''
    f.write("#----------------\n")
    f.write("#   k         chi\n")
    for (x,y) in sorted_keys:
        # There is a small edge-case bug here.
        # For floats in scientific notation, i.e. matching .*e{\d}* after being 
        # converted to a string, part or all of the 
        # exponent could be truncated.  This occurs because floats show
        # at most 12 digits of precision when converted to a string
        split_key = str(x).split('.')
        f.write("  ")
        l0 = len(split_key[0])
        f.write(split_key[0])
        f.write(".")
        if len(split_key) > 1:
            if len(split_key[1]) > (8-l0): 
                f.write(split_key[1][0:(8-l0)])
            else:
                l1 = len(split_key[1])
                f.write(split_key[1])
                f.write("0"*(8-(l0+l1)))

        f.write(" "*2)
        f.write(str(y))
        f.write("\n")
    f.close()

def make_window(f_name, **window_info):
    plt.figure()
    fig = plt.gcf()
    fig.canvas.set_window_title(os.path.basename(f_name))
    plt.title(os.path.basename(f_name))
    for attr in window_info:
        if hasattr(plt, str(attr)):
            m = getattr(plt, str(attr))
            m(window_info[str(attr)])

    x = []
    y = []
    f = open(f_name, 'r+')
    for line in f:
        if line[0] == "#" or len(line) == 0:
            continue
        s = line.split()
        x.append(float(s[0]))
        y.append(float(s[1]))
    plt.plot(x, y)
    f.close()

def find_chir(dirname, chik=default_chik, chir=default_chir):
    '''Makes a Re[chi(r)] plot given a directory and the filename of a 
    chi(k) plot.'''
    print ['perl', 'chir.ps', dirname, chik, chir]
    subprocess.call(['perl', 'chir.ps', dirname, chik, chir])

def main(f_list):
    count = 0
    for f_name in f_list:
        count += 1 
        make_window(f_name)
        if count > 50:
            break

if __name__ == '__main__':
    dirname = os.path.abspath(sys.argv[1])
    if '-s' == sys.argv[-1]: 
        sFlag = True
        f_list = sys.argv[2:-1];
    else: 
        sFlag = False
        f_list = sys.argv[2:]

    # Calculates average of f_list files, i.e. averaged chi(k)
    avg(f_list, dirname)
    # Shows it
    display_avg(dirname)

    avg_chik = dirname + '/' + default_chik
    chik = read_data(avg_chik)
    chikcubed = []
    for k in chik:
        chikcubed.append((k[0], (float(k[0])**3 * float(k[1]))))
    f = open(dirname + '/' + default_chik_cubed, 'w')
    write_data(f, chikcubed)

    chiksq = []
    for k in chik:
        chiksq.append((k[0], (float(k[0])**2 * float(k[1]))))
    f = open(dirname + '/' + default_chik_sq, 'w')
    write_data(f, chiksq)

    make_window(dirname + '/' + default_chik_sq)
    make_window(dirname + '/' + default_chik_cubed)

    if sFlag:
        main(f_list)

    # Finds chi(r) via perl script whch invokes ifeffit
    find_chir(dirname)
    # And plots it
    make_window(dirname + '/' + default_chir)
    try:
        plt.show()
    except KeyboardInterrupt:
        print "Plots closed by KeyboardInterrupt."
