import sys
import re


class CommandStringData:
    def __init__(self, sys_args: list):
        self.mode = self._validate_mode(sys_args[0])
        self.string_to_work = self._preprocessing(sys_args[1])
        self.key = self._validate_key(sys_args[2])

    @staticmethod
    def _validate_mode(mode) -> int:
        if mode == 'd':
            return -1
        elif mode == 'e':
            return 1
        else:
            error("One of two modes of operation is expected: 'e' or 'd'")

    @staticmethod
    def _validate_key(key) -> int:
        if key.isdigit():
            return int(key)
        else:
            error('Key must be an integer')

    @staticmethod
    def _preprocessing(string_to_work):
        string_to_work = " ".join(re.findall("[A-Za-z0-9]+", string_to_work))
        if string_to_work:
            return string_to_work
        else:
            error('Expected string matching [A-Za-z0-9] pattern')


def error(message):
    print(message)
    sys.exit(-1)


class Caesar:
    def __init__(self, key):
        self.key = key

    def __str__(self):
        """
             Если понадобится по-разному зашифровать разные строки,
             неплохо было бы знать ключ для каждой из них
        """
        return f"This object's key: {self.key}"

    def start(self, string, alphabet, mode):
        result = []
        step = mode*self.key
        for symbol in string:
            result.append(alphabet[(alphabet.index(symbol) + step) % len(alphabet)])
        encoded_string = ''.join(result)
        return encoded_string
