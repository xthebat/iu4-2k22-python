from typing import List

from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtWidgets import QHBoxLayout, QLabel


NicknameType = str
MessageType = list


class UserUnit:

    def __init__(self, nickname: NicknameType = "", messages: MessageType = List[str]):
        self.nickname = nickname
        self.messages = messages


class UserWidget(QtWidgets.QWidget):

    def __init__(self):
        super(UserWidget, self).__init__()
        uic.loadUi('../ui/userwidget.ui', self)

    def set_user(self, user: UserUnit):
        self.userLabel.setText(user.nickname)
        self.messagesLabel.setText(str(len(user.messages)))
        self._set_messages_list(user.messages)

    def _set_messages_list(self, messages_list: list):
        self.messagesListLabel.setText('\n\u00b7 '.join(['', *messages_list]))
