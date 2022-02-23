import itertools
from collections import Iterable, Callable
from typing import Dict, List, Tuple


def groupby(collection: Iterable, key: Callable) -> Dict:
    # groupby wants sorted collection
    sort = sorted(collection, key=key)
    groups = itertools.groupby(sort, key)
    return {key: list(value) for key, value in groups}


def parse_args(args: List[str]) -> Dict[str, str]:
    result: Dict[str, str] = dict()
    for it in args[1:]:
        splitted = it.split("=")
        if len(splitted) != 2:
            raise Exception(f"Can't parse argument {splitted}")
        name, value = splitted
        if name in result:
            raise Exception(f"Argument {name} already defined with value {value}")
        result[name] = value
    return result


def load_csv(filepath: str, delimeter: str = ",") -> List[List[str]]:
    with open(filepath, "rt", encoding="utf8") as input_file:
        return [line.split(delimeter) for line in input_file.readlines() if line.strip()]
