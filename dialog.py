import random

from PyQt6 import QtWidgets
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem

from input_window import Ui_DialogAdd


def setup_table(table: QtWidgets.QTableWidget, columns: int, rows: int, list_headers: list):
    """setup_table(table, columns, rows, list_headers) инициализирует таблицу table
       с columns стоблцами и rows рядами, а также с заголовками столбцов list_headers
    """
    table.setEnabled(True)
    table.setRowCount(0)
    table.setColumnCount(columns)
    table.setRowCount(rows)
    table.setHorizontalHeaderLabels(list_headers)
    for i in range(columns):
        (table.horizontalHeader().
         setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents))
    table.horizontalHeader().setStretchLastSection(True)


def setup_matrix(table: QtWidgets.QTableWidget, columns: int, list_headers: list):
    table.setEnabled(True)
    table.setRowCount(0)
    table.setColumnCount(columns)
    table.setRowCount(columns)
    table.setHorizontalHeaderLabels(list_headers)
    table.setVerticalHeaderLabels(list_headers)
    for i in range(columns):
        table.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
        for j in range(columns):
            if i == j:
                table.setItem(i, j, QtWidgets.QTableWidgetItem(""))
                table.item(i, j).setBackground(QColor.fromRgb(100, 0, 0))
                continue
            table.setItem(i, j, QtWidgets.QTableWidgetItem("0"))


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


class InputDialog(QtWidgets.QDialog, Ui_DialogAdd):
    """Окно ввода входных данных"""

    def __init__(self):
        super(InputDialog, self).__init__()
        self.setupUi(self)
        self.createButton.clicked.connect(self.manualCreate)

        self.tablePointInput.setRowCount(0)
        self.tableLoads.setRowCount(0)

        self.points = []
        self.edges = []
        self.packages = []
        self.loads = []
        self.channels = []
        self.routers = []
        self.correct_info = False

        self.pushButton.clicked.connect(self.ready)

        self.tableLoads.cellChanged.connect(self.on_cell_changed)

        # реализация Добавления, удаления и копирования в таблицах для входных данных
        # self.addButtonLoads.clicked.connect(lambda: load(self.tableLoads))
        # self.deleteButtonLoads.clicked.connect(lambda: rm(self.tableLoads))
        # self.copyButtonLoads.clicked.connect(lambda: cp(self.tableLoads))

        self.addButtonPackages.clicked.connect(lambda: load(self.tablePointInput))
        self.deleteButtonPackages.clicked.connect(lambda: rm(self.tablePointInput))
        self.copyButtonPackages.clicked.connect(lambda: cp(self.tablePointInput))

    def manualCreate(self):
        """Ручное добавление данных"""
        n = self.inputNumOfPoints.text()
        if not is_number(n):
            error("[manualCreate]: введёно не число")
            return
        n = int(n)
        if n <= 0:
            error("[manualCreate]: число узлов не может быть меньше или равно нулю!")
            return
        if self.checkAuto.isChecked():
            self.autoCreate(n)
            return

        setup_table(self.tablePointInput,
                    3, n, ["Имя узла", "X", "Y"])
        setup_matrix(self.tableLoads,
                     n, [str(i + 1) for i in range(n)])

    def autoCreate(self, n: int):
        setup_table(self.tablePointInput,
                    3, n, ["Имя узла", "X", "Y"])
        setup_matrix(self.tableLoads,
                     n, [str(i + 1) for i in range(n)])

        xs = [(random.randint(-n, n), random.randint(-n, n)) for _ in range(n)]
        # защита от повторяющихся данных
        xs = list(set(xs))
        while len(xs) < n:
            to_add = (random.randint(-n, n), random.randint(-n, n))
            if to_add not in xs:
                xs.append((random.randint(-n, n), random.randint(-n, n)))

        edges = []
        for i in range(len(xs) - 1):
            edges.append((i + 1, i + 2))

        price_default = "10"
        rate_default = "256"
        for i, (x, y) in enumerate(xs):
            self.tablePointInput.setItem(i, 0, QtWidgets.QTableWidgetItem(str(i + 1)))
            self.tablePointInput.setItem(i, 1, QtWidgets.QTableWidgetItem(str(x)))
            self.tablePointInput.setItem(i, 2, QtWidgets.QTableWidgetItem(str(y)))
        # for i, (x, y) in enumerate(edges):
        #     if i != 0:
        #         self.tableChannelsInput.insertRow(i)
        #     self.tableChannelsInput.setItem(i, 0, QtWidgets.QTableWidgetItem(str(x)))
        #     self.tableChannelsInput.setItem(i, 1, QtWidgets.QTableWidgetItem(str(y)))
        #     self.tableChannelsInput.setItem(i, 2, QtWidgets.QTableWidgetItem(rate_default))
        #     self.tableChannelsInput.setItem(i, 3, QtWidgets.QTableWidgetItem(price_default))

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
                    if is_number(v):
                        if int(v) < 0:
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
            error(str(e))

    def clear(self):
        self.inputNumOfPoints.clear()
        self.checkAuto.setChecked(False)

        self.tablePointInput.setRowCount(0)
        self.tableLoads.setRowCount(0)

        self.points = []
        self.edges = []
        self.packages = []
        self.loads = []
        self.channels = []
        self.routers = []
        self.correct_info = False
