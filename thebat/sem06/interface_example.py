import socket
from typing import Optional, IO, List


class FileInterface:

    def read(self, size: int) -> bytes:
        raise NotImplementedError

    def write(self, data: bytes) -> int:
        raise NotImplementedError

    def open(self, address):
        raise NotImplementedError


class SocketFile(FileInterface):

    def __init__(self):
        self.__sock = socket.socket()

    def read(self, size: int) -> bytes:
        return self.__sock.recv(size)

    def write(self, data: bytes) -> int:
        return self.__sock.send(data)

    def open(self, address):
        self.__sock.connect(address)


class CommonFile(FileInterface):

    def __init__(self):
        self.__name: Optional[str] = None
        self.__file: Optional[IO] = None

    def read(self, size: int) -> bytes:
        return self.__file.read(size)

    def write(self, data: bytes) -> int:
        return self.__file.write(data)

    def open(self, address):
        self.__name = address
        self.__file = open(self.__name)
