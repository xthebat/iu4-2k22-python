import numpy as np
import sys


def read_file(args: list) -> list:
    f = open(args[1], "r", encoding="utf-8")
    chat = f.read()
    chat_list = chat.split("\n")
    return chat_list


def main(text: list) -> None:
    names = []
    for elem in text:
        if elem != "" and "\u200b" not in elem:
            names.append(elem)
    unique, counts = np.unique(names, return_counts=True)
    result = dict(zip(unique, counts))
    sorted_result = sorted(result.items(), key=lambda x: x[1])
    print(sorted_result)

if __name__ == '__main__':
    main(read_file(sys.argv))
