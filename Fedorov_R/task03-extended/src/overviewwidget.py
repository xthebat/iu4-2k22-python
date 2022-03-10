from typing import Any, Dict
from enum import Enum

from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtCore import QObject, QAbstractTableModel, QModelIndex, Qt, pyqtSignal
from PyQt5.QtWidgets import QHeaderView

from chatprocessing import *
from userwidget import UserUnit


class TableHeader(Enum):

    NICKNAME = 0
    MESSAGES = 1
    # SENDING_TIMES = 2


class OverviewTableModel(QAbstractTableModel):

    _headers = {TableHeader.NICKNAME: "Nickname", TableHeader.MESSAGES: "Messages"}
                # TableHeaders.SENDING_TIMES: "Sending times"}

    def __init__(self):
        super(OverviewTableModel, self).__init__()
        self._data = list()

    def set_content(self, chat_data: ChatProcessingList) -> None:
        QAbstractTableModel.beginResetModel(self)
        self._data = chat_data
        QAbstractTableModel.endResetModel(self)

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self._data)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return len(TableHeader)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> Any:
        if role != QtCore.Qt.DisplayRole:
            return None
        if orientation == QtCore.Qt.Horizontal and section < len(self._headers):
            if role == QtCore.Qt.DisplayRole:
                return self._headers[TableHeader(section)]
        elif orientation == QtCore.Qt.Vertical:
            return section + 1
        return None

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        if not index.isValid():
            return Qt.NoItemFlags
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def data(self, index: QModelIndex, role: int = ...) -> Any:
        if len(self._data) == 0 or not index.isValid() or index.row() > len(self._data):
            return None
        if role == QtCore.Qt.DisplayRole:
            if index.column() == TableHeader.NICKNAME.value:
                return self._data[index.row()].nickname
            elif index.column() == TableHeader.MESSAGES.value:
                messages = self._data[index.row()].messages
                message_str = f"Total: {len(messages)} messages\n"
                message_str += "\n".join(messages)
                return message_str
            # elif index.column() == TableHeaders.SENDING_TIMES:
            #     return None
        elif role == QtCore.Qt.EditRole:
            pass
        return None

    def sort(self, column: int, order: Qt.SortOrder = ...) -> None:
        self.layoutAboutToBeChanged.emit()
        reverse = False if order == Qt.DescendingOrder else True
        if column == TableHeader.NICKNAME.value:
            self._data.sort(key=lambda x: x.nickname, reverse=reverse)
        if column == TableHeader.MESSAGES.value:
            self._data.sort(key=lambda x: len(x.messages), reverse=reverse)
        self.layoutChanged.emit()

    def insertRow(self, row: int, parent: QModelIndex = ...) -> bool:
        return True

    def removeRow(self, row: int, parent: QModelIndex = ...) -> bool:
        return True


class OverviewWidget(QtWidgets.QWidget):

    table_view_double_clicked = pyqtSignal(UserUnit)

    def __init__(self):
        super(OverviewWidget, self).__init__()
        uic.loadUi('../ui/overviewwidget.ui', self)
        self._recording_list = list()
        self._set_widgets()
        self._set_connections()

    def _set_widgets(self):
        self._chat_processing = ChatProcessing()
        self._overview_table_model = OverviewTableModel()
        self.tableView.setModel(self._overview_table_model)
        self.tableView.setSortingEnabled(True)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    def _set_connections(self):
        self.tableView.doubleClicked.connect(self.on_table_view_double_clicked)

    def process(self, recording: str) -> None:
        self._recording_list = self._chat_processing.process_list(recording)
        self._overview_table_model.set_content(self._recording_list)

    @QtCore.pyqtSlot(QModelIndex)
    def on_table_view_double_clicked(self, index: QModelIndex):
        if index.column() == TableHeader.NICKNAME.value:
            self.table_view_double_clicked.emit(self._recording_list[index.row()])
