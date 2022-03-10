from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtWidgets import QFileDialog, QGridLayout, QMenu, QAction
from PyQt5.QtCore import *

from overviewwidget import OverviewWidget
from userwidget import UserWidget, UserUnit
from chatprocessing import ChatProcessing


class CheckStatisticsMainWindow(QtWidgets.QMainWindow):
    _w = 800
    _h = 600

    def __init__(self):
        super(CheckStatisticsMainWindow, self).__init__()
        uic.loadUi('../ui/checkstatisticsmainwindow.ui', self)
        self._file_manager = FileManager(self)
        self._set_geometry()
        self._set_widgets()
        self._set_connections()
        self._set_recent_file_manager()

    def _set_geometry(self) -> None:
        rect = QtWidgets.QApplication.primaryScreen().availableGeometry()
        self.setGeometry(abs(rect.width() - self._w) / 2, abs(rect.height() - self._h) / 2, self._w, self._h)

    def _set_widgets(self) -> None:
        self._chat_processing = ChatProcessing()
        self._overview_widget = OverviewWidget()
        self._user_widget = UserWidget()
        self._overview_stacked_widget_manager = PageWidgetManager(self.overviewStackedWidget)
        self._user_stacked_widget_manager = PageWidgetManager(self.userStackedWidget)
        self._tab_widget_manager = PageWidgetManager(self.tabWidget)
        layout_overview = QGridLayout(self.overviewPage)
        layout_overview.addWidget(self._overview_widget)
        layout_user = QGridLayout(self.userPage)
        layout_user.addWidget(self._user_widget)

    def _set_connections(self) -> None:
        self.fileOpenButton.clicked.connect(self.on_file_button_clicked)
        self.chatTextEdit.textChanged.connect(self.on_chat_text_edited)
        self._overview_widget.table_view_double_clicked.connect(self.on_table_view_double_clicked)
        self.actionOpen.triggered.connect(self.on_open_file_action_triggered)
        self.actionQuit.triggered.connect(self.on_quit_action_triggered)

    def _set_recent_file_manager(self):
        self._recent_file_manager = RecentFileManager(self.menuRecent)
        self._recent_file_manager.open.connect(self.on_recent_file_opened)
        self._recent_file_manager.restore()

    @QtCore.pyqtSlot()
    def on_file_button_clicked(self) -> None:
        file = self._file_manager.open_txt()
        if file:
            self._recent_file_manager.add(file.fileName())
            self.fileNameLabel.setText(file.fileName())
            content = self._file_manager.read_txt(file)
            self.chatTextEdit.setText(content)

    @QtCore.pyqtSlot()
    def on_chat_text_edited(self) -> None:
        text = self.chatTextEdit.toPlainText()
        if text:
            self._overview_stacked_widget_manager.set_page(1)
            self._overview_widget.process(text)
        else:
            self._overview_stacked_widget_manager.set_blank_page()
            self._user_stacked_widget_manager.set_blank_page()

    @QtCore.pyqtSlot(UserUnit)
    def on_table_view_double_clicked(self, chat_unit: UserUnit) -> None:
        self._user_stacked_widget_manager.set_page(1)
        self._tab_widget_manager.set_page(1)
        self._user_widget.set_user(chat_unit)

    @QtCore.pyqtSlot()
    def on_open_file_action_triggered(self) -> None:
        file = self._file_manager.open_txt()
        if file:
            self._recent_file_manager.add(file.fileName())
            self.fileNameLabel.setText(file.fileName())
            content = self._file_manager.read_txt(file)
            self.chatTextEdit.setText(content)

    @QtCore.pyqtSlot()
    def on_open_recent_file_action_triggered(self) -> None:
        pass

    @QtCore.pyqtSlot()
    def on_quit_action_triggered(self) -> None:
        QtWidgets.QApplication.closeAllWindows()

    @QtCore.pyqtSlot()
    def on_about_action_triggered(self) -> None:
        pass

    @QtCore.pyqtSlot()
    def on_recent_file_opened(self) -> None:
        pass


class FileManager(QObject):

    def __init__(self, widget: QtWidgets.QWidget):
        super().__init__()
        self.widget = widget

    def open_txt(self):
        path = QFileDialog.getOpenFileName(self.widget.centralWidget(), "Choose File", QDir.homePath(),
                                           "Text files (*.txt)")[0]
        if not path:
            return None
        return QFile(path)

    def read_txt(self, file: QFile) -> str:
        content = ""
        if file.open(QFile.ReadOnly):
            content = bytes(file.readAll()).decode("utf-8")
            file.close()
        return content


class RecentFileManager(QObject):

    _max_size = 5
    _data = list()
    _group = "RecentFiles"
    _array = "recentFilesList"
    open = pyqtSignal()

    def __init__(self, menu: QMenu):
        super().__init__()
        self._menu = menu

    def add(self, path: str):
        if path in self._data:
            return
        self._data.append(path)
        if len(self._data) > self._max_size:
            self._data.pop()
        self.save()
        self.restore()

    def restore(self):
        settings = QSettings()
        settings.beginGroup(self._group)
        size = settings.beginReadArray(self._array)
        for i in range(size):
            if i >= self._max_size:
                break
            settings.setArrayIndex(i)
            path = str(settings.value("path"))
            self._data.append(path)
        settings.endArray()
        settings.endGroup()

        for path in self._data:
            action = QAction(path, self._menu)
            action.triggered.connect(self.on_open_action_triggered)
            action.setData(path)
            self._menu.addAction(action)
        self._menu.addSeparator()
        clear_action = QAction("Clear", self._menu)
        self._menu.addAction(clear_action)
        clear_action.triggered.connect(self.on_clear_all)

    def save(self):
        settings = QSettings()
        settings.beginGroup(self._group)
        settings.remove("")
        settings.beginWriteArray(self._array)
        for i in range(len(self._data)):
            settings.setArrayIndex(i)
            data = self._data[i]
            settings.setValue("path", data)
        settings.endArray()
        settings.endGroup()

    def clear_actions(self):
        self._menu.clear()
        self._data.clear()

    @QtCore.pyqtSlot()
    def on_clear_all(self):
        self.clear_actions()
        settings = QSettings()
        settings.beginGroup(self._group)
        settings.remove("")

    @QtCore.pyqtSlot()
    def on_open_action_triggered(self, checked: bool):
        self.open.emit()


class PageWidgetManager:

    def __init__(self, widget: QtWidgets.QWidget):
        self._widget = widget
        self.set_blank_page()

    def set_blank_page(self):
        self._widget.setCurrentIndex(0)

    def set_page(self, index: int):
        self._widget.setCurrentIndex(index)
