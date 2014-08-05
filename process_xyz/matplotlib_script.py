import matplotlib.pyplot as plt
import sys

avg_f = "avg_f.txt"

def display_avg(dir_name):
    make_window(dir_name + '/' + avg_f)

def show():
    plt.show()

def avg(f_list, dir_name):
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

    f = open(dir_name + '/' + avg_f, 'w')
    f.write("#   k         chi\n")
    for (x,y) in sorted_keys:
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

def make_window(f_name):
    plt.figure()
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

def main(f_list):
    for f_name in f_list:
        make_window(f_name)
    plt.show()

if __name__ == '__main__':
    dir_name = sys.argv[1]
    f_list = sys.argv[2:]

    avg(f_list, dir_name)
    display_avg(dir_name)
    main(f_list)
