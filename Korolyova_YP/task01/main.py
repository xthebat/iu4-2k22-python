
def main(arg: list):
    A=arg
    return A

if __name__ == '__main__':
    arg=main(["d","efghijkabcd", 4])
    str=arg[1]
    d_e=arg[0]
    key=arg[2]
    list = list(str)
    list2 = str
    j = 1
    i = len(list)
    if d_e == "e":
        while (j <= key):
            list2 = list[0]
            list.append(list2)
            list.remove(list2)
            j = j + 1
        print(''.join(list))
    if d_e == "d":
        key = i - key
        while (j <= key):
            list2 = list[0]
            list.append(list2)
            list.remove(list2)
            j = j + 1
        print(''.join(list))
