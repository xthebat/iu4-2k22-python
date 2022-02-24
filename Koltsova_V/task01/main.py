import sys

def main(args):
    #Скорее всего, это самый тупой код, который Вам доводилось видеть в жизни, но это пик мой мозговой деятельности
    alfavit_LETT = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    alfavit_NUM = '0123456789'
    sdvig = int(input('Шаг шифровки: '))
    message = input("Введите то, что хотите зашифровать: ")
    result = ''
    choice = input('Выберите что вы будете шифровать 1 - цифры или 2 - буквы: ')
    if choice == '2':
        for i in message:
            mesto = alfavit_LETT.find(i)        #Вычисляем конкретные места символов в передаваемой строке
            new_mesto = mesto + sdvig           #К каждому мсту символа прибавляем значение сдвига
            if i in alfavit_LETT:
                result += alfavit_LETT[new_mesto]
            else:
                result += i
    else:
        for i in message:
            mesto = alfavit_NUM.find(i)
            new_mesto = mesto + sdvig
            if i in alfavit_NUM:
                result += alfavit_NUM[new_mesto]
            else:
                result += i
    print(result)
    return 0


if __name__ == '__main__':
    main(sys.argv)