import sys
import os

from collections import namedtuple
from typing import List, Dict, Optional

from functions import groupby


Record = namedtuple('Record', ['author', 'comment'])


class Author(object):

    def __init__(self, name: str, comments: List[str], aka: Optional[str]):
        self.name = name
        self.comments = comments
        self.aka = aka

    def __str__(self) -> str:
        aka = "" if self.aka is None else f" aka {self.aka}"
        return f"{self.name}{aka} написал(а) {len(self.comments)} шт. комментариев на {self.symbols} шт. символов"

    @property
    def symbols(self):
        # better to be lazy
        return sum(len(it) for it in self.comments)


class Chat(object):

    @staticmethod
    def __raw2records(text: str) -> List[Record]:
        records = []
        for author_comment in text.strip().split('\n\n'):
            author_comment_split = author_comment.strip().split('\n')
            if len(author_comment_split) != 2:
                print(f"Can't parse record: {author_comment}")
                continue
            records.append(Record(author_comment_split[0], author_comment_split[1]))
        return records

    @staticmethod
    def __parse(text: str, aka: Dict[str, str] = None) -> List[Author]:
        aka = aka or dict()
        records = Chat.__raw2records(text)
        grouped = groupby(records, key=lambda it: it[0])
        return [Author(name, comments, aka.get(name, None)) for name, comments in grouped.items()]

    @classmethod
    def from_file(cls, filepath: str, aka: Dict[str, str] = None) -> "Chat":
        with open(filepath, "rt", encoding="utf8") as input_file:
            text = input_file.read()
            authors = Chat.__parse(text, aka)
            return Chat(authors)

    def __init__(self, authors: List[Author]):
        self.authors = authors

    def __str__(self):
        return "\n".join(str(author) for author in self.authors)

    def print(self):
        # lazy print
        for author in self.authors:
            print(author)


if __name__ == "__main__":
    main(sys.argv)
