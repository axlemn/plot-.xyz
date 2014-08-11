import matplotlib.pyplot as plt
import sys
import subprocess
import os

default_chi_k = "chi.k"
default_chi_r = "chi.r"

def display_avg(dirname):
    make_window(dirname + '/' + default_chi_k)

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

    f = open(dirname + '/' + default_chi_k, 'w')
    f.write("#----------------\n")
    f.write("#   k         chi\n")
    for (x,y) in sorted_keys:
        # There is a very rare bug here.
        # The bug would exist for floats in scientific notation, i.e. matching
        # .*e{\d}*, after being converted to a string.  Then part or all of the 
        # exponent would be truncated.  This occurs because floats show
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

def find_chir(dirname, chi_k=default_chi_k, chi_r=default_chi_r):
    '''Plots a Re[chi(r)] plot given a directory and the filename of a 
    chi(k) plot.'''
    print ['perl', 'chir.ps', dirname, chi_k, chi_r]
    subprocess.call(['perl', 'chir.ps', dirname, chi_k, chi_r])

def main(f_list):
    for f_name in f_list:
        make_window(f_name)
    try:
        plt.show()
    except KeyboardInterrupt:
        print "Plots closed by KeyboardInterrupt."
        exit(0)

if __name__ == '__main__':
    dirname = os.path.abspath(sys.argv[1])
    f_list = sys.argv[2:]
    avg(f_list, dirname)
    display_avg(dirname)
    find_chir(dirname)
    make_window(dirname + '/' + default_chi_r)
    plt.show()
