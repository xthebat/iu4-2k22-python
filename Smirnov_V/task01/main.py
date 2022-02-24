ENCRYPTION_CYCLE = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"

def main(arg1, arg2, arg3: str) -> str:
    k = int(arg3)  # сдвиг на число k
    if (arg1 == "e"):
        list_e = list(arg2)  #преобразование строки шифрования в список
        for i in range(0, len(arg2)):
            for j in range(0, len(ENCRYPTION_CYCLE)):
                if list_e[i] == ENCRYPTION_CYCLE[j]: 
                    list_e[i] = ENCRYPTION_CYCLE[(j+k) % len(ENCRYPTION_CYCLE)]  #вычисление смещения шифрования
                    break
        print("".join(list_e))
    elif(arg1 == "d"):
        list_d = list(arg2)  # преобразование строки дешифрования в список
        for i in range(0, len(arg2)):
            for j in range(0, len(ENCRYPTION_CYCLE)):
                if list_d[i] == ENCRYPTION_CYCLE[j]:
                    list_d[i] = ENCRYPTION_CYCLE[(j - k) % len(ENCRYPTION_CYCLE)]
                    break
        print("".join(list_d))
    else:
        print("Invalid argument. Use 'e' or 'd'")
        sys.exit(-1)


if __name__ == '__main__':
    main("e", "ABC", "1")
    main("e", "ABCrererDFSF879", "61")
    main("d", "Khoor, zruog", "3")