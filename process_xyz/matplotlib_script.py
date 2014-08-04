import matplotlib.pyplot as plt

def make_window(f_name):
    plt.figure()
    x = []
    y = []
    f = open(f_name, 'r+')
    for line in f:
        # Ignore comments
        if line[0] == "#":
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
