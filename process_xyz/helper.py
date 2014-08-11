import os
import errno

'''Contains many helper functions.  Ideally will not import libraries that are tempermental if imported multiple times.'''

def make_sure_path_exists(path):
    '''Creates a directory if it did not previously exist.'''
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def get_dirname(f, subdir=""):
    '''Takes in a filename, and returns the pathname to use to hold
    all files relating to it.'''
    base = os.path.basename(f)

    if base == "":
        raise Exception("Tried to update an invalid path name!")

    d = os.path.dirname(os.path.abspath(f))
    return d +  "/" + base[:-4] + "/" + str(subdir)

if __name__ == '__main__':
    pass
