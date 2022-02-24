import logging as logger


class InputExceptionManager:
    """Exceptions manager used for convenient handling of Input Exceptions"""
    logger_error_message = "Input data can't be processed!"

    def __init__(self):
        self.exceptions = tuple([IncorrectNumberOfParameters, IncorrectHelpValue, IncorrectDecodeEncodeValue,
                                 NotInAlphabetCharacter, IncorrectKeyValue])

    def decorate(self, func):
        def wrapper(*args, **kwargs) -> bool:
            try:
                func(*args, **kwargs)
            except self.exceptions:
                logger.exception(self.logger_error_message)
                return False
            else:
                return True
        return wrapper


class InputException(Exception):
    """Base class used for processing input data errors"""
    pass


class IncorrectNumberOfParameters(InputException):
    def __init__(self, args: list):
        self._args = args
        super().__init__("Wrong number of parameters! Expected 3 parameters,"
                         " got {} parameters instead".format((len(args)) - 1))


class IncorrectHelpValue(InputException):
    def __init__(self, args: list):
        self._args = args
        super().__init__("Expected -h/--help")


class IncorrectDecodeEncodeValue(InputException):
    def __init__(self, args: list):
        self._args = args
        super().__init__("Wrong encode/decode value! Expected 'd'/'decode' or 'e'/'encode',"
                         " got '{}' instead".format(args[1]))


class NotInAlphabetCharacter(InputException):
    def __init__(self, args: list):
        self._args = args
        super().__init__("Wrong character in '{}'! Expected upper/lower english alphabet or digits".format(args[2]))


class IncorrectKeyValue(ValueError):
    def __init__(self, args: list):
        self._args = args
        super().__init__("Wrong key value! Expected nonnegative integer value,"
                         " got '{}' instead".format(args[3]))
