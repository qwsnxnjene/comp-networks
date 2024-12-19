import random

from PyQt6 import QtWidgets
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QMessageBox

from input_window import Ui_DialogAdd


def setup_table(table: QtWidgets.QTableWidget, info_from: list, columns: int, rows: int, list_headers: list):
    """setup_table(table, columns, rows, list_headers) инициализирует таблицу table
       с columns стоблцами и rows рядами, а также с заголовками столбцов list_headers
    """
    try:
        table.setEnabled(True)
        table.setColumnCount(columns)
        table.setRowCount(rows)
        table.setHorizontalHeaderLabels(list_headers)
        for i in range(columns):
            (table.horizontalHeader().
             setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents))
            for j in range(rows):
                table.setItem(j, i, QtWidgets.QTableWidgetItem(str(info_from[j][table.horizontalHeaderItem(i).text()])))
        table.horizontalHeader().setStretchLastSection(True)
    except Exception as e:
        error(str(e))


def setup_matrix(table: QtWidgets.QTableWidget, columns: int, list_headers: list, info_from: list, points: list):
    table.setEnabled(True)
    table.setRowCount(0)
    table.setColumnCount(columns)
    table.setRowCount(columns)
    table.setHorizontalHeaderLabels(list_headers)
    table.setVerticalHeaderLabels(list_headers)
    print(info_from)
    for i in range(columns):
        (table.horizontalHeader().
         setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch))
        for j in range(columns):
            table.setItem(i, j, QtWidgets.QTableWidgetItem(""))
            if i == j:
                table.item(i, j).setBackground(QColor.fromRgb(100, 0, 0))

    for load in info_from:
        fr, to = -999, -999
        for point in points:
            if point['Имя узла'] == load['Из узла']:
                fr = int(point['Номер'])
            if point['Имя узла'] == load['В узел']:
                to = int(point['Номер'])
            if fr != -999 and to != -999:
                break
        if fr != -999 and to != -999:
            table.setItem(fr - 1, to - 1, QtWidgets.QTableWidgetItem(str(load['Объём информации(в Байт/c)'])))

    for i in range(columns):
        for j in range(columns):
            if i != j and table.item(i, j).text() == "":
                table.setItem(i, j, QtWidgets.QTableWidgetItem("-"))


def error(message: str):
    """error(message) выводит сообщение message в появляющемся окне"""
    msgBox = QMessageBox()
    msgBox.setWindowTitle("Внимание!")
    # message = message.split(':')[1][1:].capitalize()
    msgBox.setText(message)
    msgBox.exec()


def is_number(n: str):
    """is_number(n) Проверяет, является ли n числом"""
    if len(n) == 0 or (n[0] == '-' and any(x.isdigit() is False for x in n[1:])
                       or (n[0] != '-' and any(x.isdigit() is False for x in n))):
        return False
    return True


def load(table: QtWidgets.QTableWidget):
    table.insertRow(table.currentRow() + 1)


def rm(table: QtWidgets.QTableWidget):
    if table.rowCount() > 0:
        table.removeRow(table.currentRow())


def cp(table: QtWidgets.QTableWidget):
    table.insertRow(table.rowCount())
    row_count = table.rowCount()
    column_count = table.columnCount()

    for j in range(column_count):
        if not table.item(row_count - 2, j) is None:
            table.setItem(row_count - 1, j,
                          QtWidgets.QTableWidgetItem(table.item(row_count - 2, j).text()))


class EditDialog(QtWidgets.QDialog, Ui_DialogAdd):
    """Окно ввода входных данных"""

    def __init__(self, points, routers, channels, packages, loads):
        super(EditDialog, self).__init__()
        self.setupUi(self)
        self.labelInput.setVisible(False)
        self.inputNumOfPoints.setVisible(False)
        self.createButton.setVisible(False)
        self.checkAuto.setVisible(False)

        self.tablePointInput.setRowCount(0)
        self.tableLoads.setRowCount(0)
        self.tableChannelsInput.setRowCount(0)
        self.tableRoutersInput.setRowCount(0)
        self.tablePackagesInput.setRowCount(0)

        self.points = points
        self.packages = packages
        self.loads = loads
        self.channels = channels
        self.routers = routers
        self.correct_info = False

        setup_table(self.tablePointInput, self.points, 3, len(self.points), ["Имя узла", "X", "Y"])
        setup_table(self.tablePackagesInput, self.packages, 1,
                    len(self.packages), ["Размер пакета(в байтах)"])
        setup_table(self.tableChannelsInput, self.channels, 4,
                    len(self.channels), ["Узел 1", "Узел 2", "Пропускная способность", "Стоимость"])
        setup_table(self.tableRoutersInput, self.routers, 3,
                    len(self.routers), ["Модель", "Пропускная способность", "Стоимость"])
        setup_matrix(self.tableLoads, len(self.points), [str(i + 1) for i in range(len(self.points))],
                     self.loads, self.points)

        self.pushButton.clicked.connect(self.ready)

        self.addButtonPackages.clicked.connect(lambda: load(self.tablePackagesInput))
        self.deleteButtonPackages.clicked.connect(lambda: rm(self.tablePackagesInput))
        self.copyButtonPackages.clicked.connect(lambda: cp(self.tablePackagesInput))

        self.addButtonChannels.clicked.connect(lambda: load(self.tableChannelsInput))
        self.deleteButtonChannels.clicked.connect(lambda: rm(self.tableChannelsInput))
        self.copyButtonChannels.clicked.connect(lambda: cp(self.tableChannelsInput))

        self.addButtonRouters.clicked.connect(lambda: load(self.tableRoutersInput))
        self.deleteButtonRouters.clicked.connect(lambda: rm(self.tableRoutersInput))
        self.copyButtonRouters.clicked.connect(lambda: cp(self.tableRoutersInput))

    def ready(self):
        try:
            names_of_points = []

            self.points = []
            self.packages = []
            self.loads = []
            self.channels = []
            self.routers = []

            row_count = self.tablePointInput.rowCount()
            column_count = self.tablePointInput.columnCount()

            # Проверка Информации об узлах
            for i in range(row_count):
                tmp = dict()
                for j in range(column_count):
                    v = self.tablePointInput.item(i, j).text()
                    if j != 0 and is_number(v):
                        tmp[self.tablePointInput.horizontalHeaderItem(j).text()] = int(v)
                    elif j == 0:
                        if len(v) == 0:
                            error("Имя узла не может быть пустым!")
                            return
                        if v in names_of_points:
                            error("Имя узла не может дублироваться!")
                            return
                        tmp[self.tablePointInput.horizontalHeaderItem(j).text()] = v
                        names_of_points.append(v)
                    else:
                        error(f"Неверный формат информации об узлах! Строчка {i + 1},"
                              f" столбец {self.tablePointInput.horizontalHeaderItem(j).text()}")
                        return
                tmp['Номер'] = str(i + 1)
                self.points.append(tmp)

            # Проверка Списка пакетов
            row_count = self.tablePackagesInput.rowCount()
            column_count = self.tablePackagesInput.columnCount()
            for i in range(row_count):
                tmp = dict()
                for j in range(column_count):
                    v = self.tablePackagesInput.item(i, j).text()
                    if is_number(v):
                        if int(v) <= 0:
                            error(
                                f"Неверный формат информации о пакетах!\n Отрицательный размер пакета! Строка {i + 1}")
                            return
                        tmp[self.tablePackagesInput.horizontalHeaderItem(j).text()] = int(v)
                    else:
                        error(f"Неверный формат информации о пакетах! Строка {i + 1}")
                        return
                self.packages.append(tmp)

            # Проверка Матрицы нагрузки
            row_count = self.tableLoads.rowCount()
            column_count = self.tableLoads.columnCount()
            for i in range(row_count):
                tmp = dict()
                for j in range(column_count):
                    v = self.tableLoads.item(i, j).text()
                    if v == '0' or v == '-':
                        continue
                    if is_number(v):
                        if int(v) <= 0:
                            error(f"Отрицательный объём информации в {i + 1} строке {j + 1} столбце матрицы нагрузки")
                            return
                        tmp['Из узла'] = [point['Имя узла'] for point in self.points if point['Номер'] == str(i + 1)][0]
                        tmp['В узел'] = [point['Имя узла'] for point in self.points if point['Номер'] == str(j + 1)][0]
                        tmp['Объём информации(в Байт/c)'] = int(v)
                    elif v == '':
                        continue
                    else:
                        error(f"Некорректный объём информации в {i + 1} строке {j + 1} столбце матрицы нагрузки")
                        return
                    self.loads.append(tmp)
                    tmp = dict()

            # Проверка Информации о каналах
            row_count = self.tableChannelsInput.rowCount()
            column_count = self.tableChannelsInput.columnCount()
            channels_name = []
            for i in range(row_count):
                tmp = dict()
                for j in range(column_count):
                    v = self.tableChannelsInput.item(i, j).text()
                    if j > 1:
                        if is_number(v):
                            if int(v) <= 0:
                                error(f"Отрицательная {self.tableChannelsInput.horizontalHeaderItem(j).text()}"
                                      f" в {i + 1} строке информации о каналах!")
                                return
                            tmp[self.tableChannelsInput.horizontalHeaderItem(j).text()] = v
                        else:
                            error(f"Некорректная {self.tableChannelsInput.horizontalHeaderItem(j).text()} "
                                  f"в {i + 1} строке информации о каналах!")
                            return
                    else:
                        if v not in names_of_points:
                            error(f"Узла, указанного в {i + 1} строке информации о каналах нет в списке узлов")
                            return
                        tmp[self.tableChannelsInput.horizontalHeaderItem(j).text()] = v

                edge = (tmp["Узел 1"], tmp["Узел 2"])
                if edge in channels_name:
                    error("Каналы не могут дублироваться!")
                    return
                if tmp["Узел 1"] == tmp["Узел 2"]:
                    error("Канал не может начинаться и заканчиваться в одном и том же узле")
                    return
                channels_name.append(edge)
                self.channels.append(tmp)

            # Проверка Доступных маршрутизаторов
            row_count = self.tableRoutersInput.rowCount()
            column_count = self.tableRoutersInput.columnCount()
            names = []
            for i in range(row_count):
                tmp = dict()
                for j in range(column_count):
                    v = self.tableRoutersInput.item(i, j).text()
                    if j != 0:
                        if is_number(v):
                            if int(v) <= 0:
                                error(f"Отрицательная {self.tableRoutersInput.horizontalHeaderItem(j).text()}"
                                      f" в {i + 1} строке доступных маршрутизаторов!")
                                return
                            tmp[self.tableRoutersInput.horizontalHeaderItem(j).text()] = v
                        else:
                            error(f"Некорректная {self.tableRoutersInput.horizontalHeaderItem(j).text()}"
                                  f" в {i + 1} строке доступных маршрутизаторов!")
                            return
                    else:
                        if len(v) == 0:
                            error("Название модели маршрутизатора не может быть пустым!")
                            return
                        if v in names:
                            error("Название модели маршрутизатора не может дублироваться!")
                            return
                        names.append(v)
                        tmp[self.tableRoutersInput.horizontalHeaderItem(j).text()] = v
                self.routers.append(tmp)
                self.correct_info = True
                self.close()
        except Exception as e:
            print(str(e))

    def clear(self):
        self.tablePointInput.setRowCount(0)
        self.tableLoads.setRowCount(0)
        self.tableChannelsInput.setRowCount(0)
        self.tableRoutersInput.setRowCount(0)
        self.tablePackagesInput.setRowCount(0)

        self.points = []
        self.packages = []
        self.loads = []
        self.channels = []
        self.routers = []
        self.correct_info = False
