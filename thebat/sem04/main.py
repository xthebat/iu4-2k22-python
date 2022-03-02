import sys
from typing import List


def key_sort(it):
    return int(it.strip(), base=16)


def convert_hex_numbers(values: List[str]) -> List[int]:
    result = []
    for index in range(len(values)):
        value = int(values[index], 16)
        result.append(value)
    return result


def lists(args):
    internal_list = ["test", "x", "y"]

    strings = [" 000", " ea ", " cd ", " aa ", "bb ", "10"]

    # strings.sort()

    # sorted_strings1 = sorted(strings, reverse=True)
    # sorted_strings2 = sorted(strings, key=lambda it: int(it.strip(), base=16), reverse=True)
    # sorted_strings3 = sorted(strings, key=key_sort, reverse=True)
    #
    # print(sorted_strings1)
    # print(sorted_strings2)
    # print(sorted_strings3)

    copy = strings.copy()

    print(copy)
    internal_list.append("34234234")
    print(copy)
    copy.extend(strings)
    print(copy)

    filter_strings = filter(lambda it: " " not in it, strings)
    hex_numbers = map(lambda it: int(it, 16), filter_strings)

    print(list(hex_numbers))

    hex_numbers = [int(it, 16) for it in strings if " " not in it]
    print(hex_numbers)

    # first_good_value = next(it for it in strings if " " not in it)
    # print(first_good_value)

    found_good_value = next((it for it in strings if " " not in it), None)
    print(found_good_value)

    print("range(10)")

    for it in range(10):  # 0, 1, 2, ... 9
        print(it)

    print("range(2, 8, 2)")

    for it in range(2, 8, 2):
        print(it)

    print(list(filter(lambda it: it > 2, range(2, 8, 2))))

    list_of_lists = [[], [], []]

    for index, item in enumerate(list_of_lists):
        item.append(index)
        print(f"{index}. {item}")

    print(list_of_lists)

    print(args)
    print(args[1:])

    print("args[:-1]")
    print(args[:-1])

    print("args[2:6:2]")

    print(args[2:6:2])

    index_of_first = args.index('first')
    print(args[index_of_first:])

    print(args[-1])


def main(args: List[str]):
    # lists(args)

    d = {
        "bat": "Alexei Glakikh",
        "bobri": "Ilya Komlev"
    }

    print(d)

    d["test"] = "Ivan Ivanov"

    print(d)

    print(d["bat"])

    strings = [" 000", " ea ", " cd ", " aa ", "bb ", "10"]

    hex_dict = {it: int(it, 16) for it in strings if " " not in it}
    print(hex_dict)

    for key, value in hex_dict.items():
        print(key, value)

    hex_dict[40] = 20

    if 40 in hex_dict:
        print("40 in hex_dict")

    pseudos = dict()

    # cmd + /
    # if "bat" not in pseudos:
    #     pseudos["bat"] = list()
    # pseudos["bat"].append("...")

    if "bat" in pseudos:
        print(pseudos["bat"])

    print(pseudos.get("bat", None))

    print(pseudos)
    bat_pseudos = pseudos.setdefault("bat", list())
    print(pseudos)
    bat_pseudos.append("fdsfaa")
    print(pseudos)

    {
        "<YT_USER_NAME>": [Comments],
        "<YT_USER_NAME>": [Comments],
        "<YT_USER_NAME>": [Comments],
    }

    {
        "<YT_USER_NAME>": "REAL_NAME"
    }

    "<YT_USER_NAME> aka REAL_NAME кол-во комментарие, кол-во символов:" \
    "- comment1" \
    "- comment2"

    open(filename, "rt").read()


if __name__ == '__main__':
    main(sys.argv)