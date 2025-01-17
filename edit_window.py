import random

from PyQt6 import QtWidgets
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem

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

        self.points = points
        self.packages = packages
        self.loads = loads
        self.channels = channels
        self.routers = routers
        self.correct_info = False

        self.tableLoads.cellChanged.connect(self.on_cell_changed)

        setup_table(self.tablePointInput, self.points, 3, len(self.points), ["Имя узла", "X", "Y"])
        setup_matrix(self.tableLoads, len(self.points), [str(i + 1) for i in range(len(self.points))],
                     self.loads, self.points)

        self.pushButton.clicked.connect(self.ready)

        self.addButtonPackages.clicked.connect(lambda: load(self.tablePointInput))
        self.deleteButtonPackages.clicked.connect(lambda: rm(self.tablePointInput))
        self.copyButtonPackages.clicked.connect(lambda: cp(self.tablePointInput))

    def on_cell_changed(self, row, col):
        # Получаем значение из измененной ячейки
        item = self.tableLoads.item(row, col)
        if item:
            value = item.text()

            # Устанавливаем симметричное значение
            symmetric_item = self.tableLoads.item(col, row)
            if not symmetric_item:
                symmetric_item = QTableWidgetItem()
                self.tableLoads.setItem(col, row, symmetric_item)
            symmetric_item.setText(value)

            # Блокируем сигналы, чтобы избежать рекурсии
            self.tableLoads.blockSignals(True)
            symmetric_item.setText(value)
            self.tableLoads.blockSignals(False)

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
            self.correct_info = True
            self.close()
        except Exception as e:
            print(str(e))

    def clear(self):
        self.tablePointInput.setRowCount(0)
        self.tableLoads.setRowCount(0)

        self.points = []
        self.packages = []
        self.loads = []
        self.channels = []
        self.routers = []
        self.correct_info = False
