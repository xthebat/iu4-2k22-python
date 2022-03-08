import sys
import functools
from collections import defaultdict
from enum import Enum
from typing import Dict, List


NicknameType = str
MessagesType = list
AssotiationType = Dict[NicknameType, NicknameType]
ChatType = Dict[NicknameType, MessagesType]


class CSVUserUnit(Enum):
    REAL_NAME = 1
    NICKNAME = 3


class FileDecorator:

    @staticmethod
    def open_file(func):
        @functools.wraps(func)
        def wrapper(self, filename, *args, **kwargs):
            try:
                with open(filename, 'r') as f:
                    return func(self, f.read(), *args, **kwargs)
            except OSError:
                print(f"Error in {filename}! No such file")
        return wrapper


class FileObject:

    @FileDecorator.open_file
    def parse(self, content: str):
        raise NotImplementedError


class AssotiationsMaker(FileObject):

    def __init__(self):
        self.parsed_content = defaultdict(MessagesType)

    @FileDecorator.open_file
    def parse(self, content: str):
        self.parsed_content.clear()
        splitted_content = content.split('\n')
        splitted_content = [s for s in splitted_content if s != '']
        for line in splitted_content[1:]:
            words = line.split(',')
            self.parsed_content[words[CSVUserUnit.REAL_NAME.value]] = words[CSVUserUnit.NICKNAME.value]
        return dict(self.parsed_content)


class ChatParser(FileObject):

    def __init__(self):
        self.parsed_recording = defaultdict(MessagesType)

    @FileDecorator.open_file
    def parse(self, content: str):
        self.parsed_recording.clear()
        recording_list = content.replace('\u200b', '').split('\n')
        recording_list = [s for s in recording_list if s != '']
        for i in range(0, len(recording_list), 2):
            self.parsed_recording[recording_list[i]].append(recording_list[i + 1])
        return dict(self.parsed_recording)


class Statistics:

    def __init__(self):
        self.maker = AssotiationsMaker()
        self.parser = ChatParser()

    def process(self, assotiations_file: str, chat_file: str):
        res = ""
        assotiations = self.maker.parse(assotiations_file)
        chat = self.parser.parse(chat_file)
        for nickname, messages in chat.items():
            count = sum(len(message) for message in messages)
            if nickname in list(assotiations.keys()):
                name = assotiations[nickname]
                res += f"{nickname} " + (f"aka {name} " if name else "") + f"with {len(messages)} comments and " \
                                                                           f"{count} symbols:\n"
                for message in messages:
                    res += "\u00b7 " + message + "\n"
            elif nickname in list(assotiations.values()):
                req_name = ""
                for name, nick in assotiations.items():
                    if nick == nickname:
                        req_name = name
                res += f"{nickname} aka {req_name} with {len(messages)} comments and {count} symbols:\n"
                for message in messages:
                    res += "\u00b7 " + message + "\n"
            else:
                res += f"User with name {nickname} wasn't found in csv table\n"
        return res


def main(args: List[str]):
    stats = Statistics()
    print(stats.process(args[1], args[2]))


if __name__ == '__main__':
    main(['parser.py', 'tes2.txt', 'tes.txt'])
    # main(sys.argv)
