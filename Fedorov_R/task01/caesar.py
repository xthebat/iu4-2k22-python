import exceptions as ex

from enum import Enum
import re
import string
import sys


class CipherDirection(Enum):
    ENCODE = 0
    DECODE = 1


class CaesarCipher:
    """Class implementing the Caesar Cipher"""
    DIRECTION_NAME = {CipherDirection.ENCODE: ("e", "encode"), CipherDirection.DECODE: ("d", "decode")}
    ALPHABET_PATTERN = "[A-Za-z0-9\s]+"

    def encode(self, string_to_work: str, key: int) -> str:
        return self._shift(string_to_work, key)

    def decode(self, string_to_work: str, key: int) -> str:
        return self._shift(string_to_work, -key)

    def _shift(self, string_to_work: str, key: int) -> str:
        res = ""
        for ch in string_to_work:
            if ch.isspace():
                res += " "
                continue
            alphabet_list = string.digits if ch.isdigit() \
                else string.ascii_lowercase if ch.islower() \
                else string.ascii_uppercase
            idx = alphabet_list.find(ch)
            res += alphabet_list[(idx + key) % len(alphabet_list)]
        return res


class InputHandler:
    """Class used for processing input"""
    _exception_manager = ex.InputExceptionManager()

    def __init__(self):
        self._output_handler = OutputHandler()

    def _validate(self, condition: bool, exception: Exception) -> None:
        if not condition:
            raise exception

    @_exception_manager.decorate
    def process_input(self, args: list) -> None:
        self._validate(len(args) in (2, 4), ex.IncorrectNumberOfParameters(args))
        if len(args) == 2:
            self._validate_two_parameters(args)
        elif len(args) == 4:
            self._validate_four_parameters(args)

    def _validate_two_parameters(self, args: list) -> None:
        self._validate(args[1] in ("-h", "--help"), ex.IncorrectHelpValue(args))
        self._output_handler.output_help()

    def _validate_four_parameters(self, args: list) -> None:
        connected_tuple = CaesarCipher.DIRECTION_NAME[CipherDirection.ENCODE] + \
                          CaesarCipher.DIRECTION_NAME[CipherDirection.DECODE]
        self._validate(args[1] in connected_tuple, ex.IncorrectDecodeEncodeValue(args))
        self._validate(re.fullmatch(CaesarCipher.ALPHABET_PATTERN, args[2]), ex.NotInAlphabetCharacter(args))
        args[3] = int(args[3])
        self._validate(isinstance(args[3], int) or args[3] < 3, ex.IncorrectKeyValue(args))


class OutputHandler:
    help_message = """usage: caesar.py mode string-to-work key
    
positional arguments:
  mode             method used to process the string-to-work using the Caesar cipher 'd' to decode, 'e' to encode
  string-to-work   string processed using the caesar cipher
  key              shift in the caesar cipher"""

    def output_help(self) -> None:
        print(self.help_message)


if __name__ == '__main__':
    input_handler = InputHandler()
    sys_arg = sys.argv
    if input_handler.process_input(sys_arg):
        caesar_cipher = CaesarCipher()
        if sys_arg[1] in CaesarCipher.DIRECTION_NAME[CipherDirection.ENCODE]:
            print(caesar_cipher.encode(sys_arg[2], int(sys_arg[3])))
        elif sys_arg[1] in CaesarCipher.DIRECTION_NAME[CipherDirection.DECODE]:
            print(caesar_cipher.decode(sys_arg[2], int(sys_arg[3])))
