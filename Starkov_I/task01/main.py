import sys
import re

TOKEN_PATTERN = "[A-Za-z0-9]+"
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"


def error(message):
    print(message)
    sys.exit(-1)


class Caesar:
    def __init__(self, input_data: list, alphabet=ALPHABET):
        self.mode = self._validate_mode(input_data[0])
        self.string_to_work = self._preprocessing(input_data[1])
        self.key = self._validate_key(input_data[2])
        self.alphabet = alphabet

    def __str__(self):
        """
             Если понадобится по-разному зашифровать разные строки,
             неплохо было бы знать ключ для каждой из них
        """
        return f"This object's key: {self.key}"

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
        try:
            return int(key)
        except ValueError:
            error('Key must be an integer')

    @staticmethod
    def _preprocessing(string_to_work):
        string_to_work = " ".join(re.findall(TOKEN_PATTERN, string_to_work))
        if string_to_work:
            return string_to_work
        else:
            error('Expected string matching [A-Za-z0-9] pattern')

    def start(self):
        pass

    def get_result(self):
        pass


def main(args: list):
    if len(args) != 4:
        error("Three arguments are expected")
    encryption = Caesar(args[1:])
    print(encryption)
    # encryption.start()


if __name__ == '__main__':
    main(sys.argv)
