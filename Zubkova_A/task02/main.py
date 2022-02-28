import sys
import os


def file(path, level=1):
    print('level=', level, 'Content:', os.listdir(path))
    for i in os.listdir(path):
        if os.path.isdir(path+'\\'+i):
            print('entrance', path+'\\'+i)
            file(path+'\\'+i, level+1)
            print('output', path)


def main(args):
    path = args[1]
    file(path)


if __name__ == '__main__':
    main(["main.py", ".\level1\level11"])
    main(sys.argv)