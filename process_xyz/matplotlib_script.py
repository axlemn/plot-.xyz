import matplotlib.pyplot as plt
import sys
import subprocess
import os
from helper import *

def avg_chik(f_list, dirname):
    count = len(f_list)
    d = {}
    d_init_flag = True
    for f_name in f_list:
        print '*',
        print f_name 
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
    '''Writes sorted_keys for matplotlib to read to file object f, then 
    closes f.'''
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

def plot_chik(exp_k):
    '''Makes window with chi(k).'''

    avg_chik = dirname + '/' + default_chik
    if exp_k == 0:
        make_window(avg_chik)
        return

    chik = read_data(avg_chik)
    chik_exp = []
    for k in chik:
        chik_exp.append((k[0], (float(k[0])**exp_k * float(k[1]))))

    f = open(dirname + '/' + default_chik + '_kexp_' + str(exp_k), 'w')
    f_name = f.name
    write_data(f, chik_exp)

    make_window(f_name)

def show_windows():
    try:
        plt.show()
    except KeyboardInterrupt:
        print "Plots closed by KeyboardInterrupt."

def plot_files(f_list):
    count = 0
    for f_name in f_list:
        count += 1 
        make_window(f_name)
        if count > 50:
            break

def find_chir(dirname, chik=default_chik, chir=default_chir):
    '''Makes a Re[chi(r)] plot given a directory and the filename of a 
    chi(k) plot.'''
    to_call = ['perl',
                os.path.dirname(os.path.realpath(__file__)) + '/chir.ps', 
                dirname, 
                chik, 
                chir]
    print '\nCalculating chi(r):'
    print ' '.join(to_call)
    subprocess.call(to_call)

def main(f_list, aFlag=False, rFlag=False, kFlag=False):
    if aFlag == True:
        # Calculates average of f_list files, i.e. averaged chi(k)
        avg_chik(f_list, dirname)
    if kFlag == True:
        # Show chik with kexp 3:
        plot_chik(3)
    if rFlag == True:
        # Finds chi(r) via perl script whch invokes ifeffit
        # And plots it
        find_chir(dirname)
        make_window(dirname + '/' + default_chir)

    show_windows()

if __name__ == '__main__':
    dirname = os.path.abspath(sys.argv[1])
    nfiles = int(sys.argv[2])
    f_list = sys.argv[3:3+nfiles]
    flags = sys.argv[3+nfiles:]

    aFlag = False
    rFlag = False
    kFlag = False
    if '-a' in flags:
        aFlag = True
    if '-r' in flags:
        rFlag = True
    if '-k' in flags:
        kFlag = True

    main(f_list, aFlag, rFlag, kFlag)
