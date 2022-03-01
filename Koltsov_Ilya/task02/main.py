import os
import sys


# Directory tree generator by Ilya Koltsov
# Works only with full filepaths

def tree(directory, padding, print_files=False):
    print(padding[:-1] + os.path.basename(os.path.abspath(directory)) + '/')
    padding = padding + ' '
    files = []
    if print_files:
        files = os.listdir(directory)
    else:
        files = [x for x in os.listdir(directory) if os.path.isdir(directory + os.path.sep + x)]
    count = 0
    for file in files:
        count += 1
        print(padding + '|')
        path = directory + os.path.sep + file
        if os.path.isdir(path):
            if count == len(files):
                tree(path, padding + '-', print_files)
            else:
                tree(path, padding + '|', print_files)
        else:
            print(padding + '├──>' + file)


def brief():
    return '''How to Use: %s <FILEPATH> [-pf] 
Print tree structure (w or w/o the included files) of the specified path.
Parameters:
<FILEPATH>  Full filepath to process
[-pf]       Print files as well as directories'''


def main(args: list):
    path = args[1]
    if len(args) == 2:
        # only print  directories
        os.chdir()
        if os.path.isdir(path):
            tree(path, ' ')
        else:
            print('ERROR: \'' + path + '\' is not a full directory')
    elif len(args) == 3 and args[2] == '-pf':
        # print directories and files
        if os.path.isdir(path):
            tree(path, ' ', True)
        else:
            print('ERROR: \'' + path + '\' is not a full directory')
    else:
        print(brief())


if __name__ == '__main__':
    main(sys.argv)
