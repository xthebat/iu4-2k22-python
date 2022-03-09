import random
import sys
from typing import Iterable


class MegaJsonParserError(Exception):
    pass


class IntParsingError(Exception):
    
    def __init__(self, value, index):
        self.value = value
        self.index = index



def json_parse(config: dict):
    try:
        text = config["text"]
        return MegaJsonParser.parse(text)
    except MegaJsonParserError as error:
        return None


def get_value_or_none(d: dict, k: str):
    try:
        v = d[k]
    except KeyError as error:
        print(f"Key {error} not found in dictionary")
        return None
    else:
        print(f"Key '{k}' found in dictionary")
        return d[v]

    # if k in d:
    #     return d[k]
    # else:
    #     return None


def main1():
    d = {
        "key0": "key1",
        "key1": 1,

        "key2": "key3",
        "key3": 3,

        "key4": "key6",
        "key5": 5
    }
    v = get_value_or_none(d, "key2")
    if v is None:
        print("first key not found!")
    else:
        print(f"nested value found: {v}")


def atoi(value: str) -> int:
    try:
        return int(value)
    except ValueError:
        return -1


def convert_int(value: str, index: int) -> int:
    try:
        return int(value)
    except ValueError:
        raise IntParsingError(value, index)


def sum_of_strings_bad(values: Iterable[str]):
    return sum(atoi(it) for it in values)


def sum_of_strings(values: Iterable[str]):
    return sum(convert_int(it, index) for index, it in enumerate(values))


def main2(args):
    values = args[1:]
    try:
        result = sum_of_strings(values)
    except ValueError as error_value:
        print(f"Can't convert: '{error_value}' for list: {values}")
    else:
        print(f"sum of {values} = {result}")


def main3_good_daemon(args):
    values = args[1:]
    try:
        result = sum_of_strings(values)
    except Exception as error:
        print(f"Error occurred {error} for: {values}")
    else:
        print(f"sum of {values} = {result}")
    finally:
        print("Program finished!")


def main5_sql(args):
    db = connect()
    try:
        return db.sql()
    finally:
        db.disconnect()


def main4_very_bad(args):
    values = args[1:]
    try:
        result = sum_of_strings(values)
    except:
        pass
    else:
        print(f"sum of {values} = {result}")


def main_with_convert(args):
    values = args[1:]
    try:
        result = sum_of_strings(values)
    except IntParsingError as error:
        s = ", ".join(values)
        print(f"Can't convert argument: '{error.value}' with index {error.index + 1} into integer for list: {s}")
    except ValueError as error:
        # ... handle other exception
    else:
        print(f"sum of {values} = {result}")


if __name__ == '__main__':
    # main1()
    main_with_convert(sys.argv)
