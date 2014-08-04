import matplotlib.pyplot as plt

def main():
    f_name = "data.tmp"
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
    plt.show()
    f.close()

if __name__ == '__main__':
    main()
