from typing import List, Dict, Optional

from functions import parse_args, load_csv
from youtube_parser import Chat


def parse_aka(aka_path: str) -> Optional[Dict[str, str]]:
    if aka_path is not None:
        csv = load_csv(aka_path)
        return {line[3]: line[1] for line in csv[1:]}
    else:
        return None


def main(args: List[str]):
    args = parse_args(args)
    input_path = args["input"]
    # output_path = args["output"]  # not implemented
    aka_path = args.get("aka", None)

    aka = parse_aka(aka_path)

    chat = Chat.from_file(input_path, aka)

    chat.print()


if __name__ == "__main__":
    # main(sys.argv)
    main(['', 'input=comments_example.txt', 'aka=aka.csv'])
