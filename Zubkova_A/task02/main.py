import sys
import os


def tree(path, level=1):
    print('level=', level, 'Content:', os.listdir(path))
    for index in os.listdir(path):
        if os.path.isdir(os.path.join(path, index)):
            print('entrance', os.path.join(path, index))
            tree(os.path.join(path, index), level+1)
            print('output', path)


def main(args):
    path = args[1]
    tree(path)


if __name__ == '__main__':
    main(["main.py", ".\level1\level11"])
    main(sys.argv)