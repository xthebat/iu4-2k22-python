import sys
from typing import Tuple


def square(value: int) -> int:
    return value * value


def get_point(string: str) -> Tuple[int, int]:
    return 10, 20


def main(args: list) -> None:
    int_var = int("1")
    int_var = 1
    int_var = 2

    float_var = 2.0
    float_var = float("2.0")
    float_var = float(2)

    str_var = "string"
    str_var = str(2)
    str_var = str(2.0)  # "2.0"
    str_var += "string2"  # "2.0string2"

    bytes_var = b"fdsfs\x00\x12"

    list_var = list([1, 2, 3])
    list_var = [1, 2, 3]

    list_var[1] = 1
    list_var.append(10)
    list_var.append(12)
    list_var.remove(10)
    print(list_var)

    tuple_var = tuple([1, 2, 3])
    tuple_var = (1, 2, 3)
    tuple_var = 1, 2, 3

    tuple_var += 1


    print("Hello world")
    print('Hello world')
    print(args)

    for item in args:
        print(item)

    print(args[1])

    square(10)

    return None


if __name__ == '__main__':
    main(sys.argv)
