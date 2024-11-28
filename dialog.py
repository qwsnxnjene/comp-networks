import random

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMessageBox

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


def read(table: QtWidgets.QTableWidget, out: list):
    row_count = table.rowCount()
    column_count = table.columnCount()

    for i in range(row_count):
        tmp = dict()
        for j in range(column_count):
            v = table.item(i, j)


class InputDialog(QtWidgets.QDialog, Ui_DialogAdd):
    """Окно ввода входных данных"""

    def __init__(self):
        super(InputDialog, self).__init__()
        self.setupUi(self)
        self.createButton.clicked.connect(self.manualCreate)

        self.points = []
        self.edges = []
        self.packages = []
        self.loads = []
        self.channels = []
        self.routers = []
        self.correct_info = False

        self.pushButton.clicked.connect(self.ready)

        # реализация Добавления, удаления и копирования в таблицах для входных данных
        self.addButtonLoads.clicked.connect(lambda: load(self.tableLoads))
        self.deleteButtonLoads.clicked.connect(lambda: rm(self.tableLoads))
        self.copyButtonLoads.clicked.connect(lambda: cp(self.tableLoads))

        self.addButtonPackages.clicked.connect(lambda: load(self.tablePackagesInput))
        self.deleteButtonPackages.clicked.connect(lambda: rm(self.tablePackagesInput))
        self.copyButtonPackages.clicked.connect(lambda: cp(self.tablePackagesInput))

        self.addButtonChannels.clicked.connect(lambda: load(self.tableChannelsInput))
        self.deleteButtonChannels.clicked.connect(lambda: rm(self.tableChannelsInput))
        self.copyButtonChannels.clicked.connect(lambda: cp(self.tableChannelsInput))

        self.addButtonRouters.clicked.connect(lambda: load(self.tableRoutersInput))
        self.deleteButtonRouters.clicked.connect(lambda: rm(self.tableRoutersInput))
        self.copyButtonRouters.clicked.connect(lambda: cp(self.tableRoutersInput))

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
        setup_table(self.tableLoads,
                    3, 1, ["Из узла", "В узел", "Объём информации(в Бит/c)"])
        setup_table(self.tablePackagesInput,
                    1, 1, ["Размер пакета(в битах)"])
        setup_table(self.tableChannelsInput,
                    4, 1, ["Узел 1", "Узел 2", "Пропускная способность", "Стоимость"])
        setup_table(self.tableRoutersInput,
                    3, 1, ["Модель", "Пропускная способность", "Стоимость"])

    def autoCreate(self, n: int):
        setup_table(self.tablePointInput,
                    3, n, ["Имя узла", "X", "Y"])
        setup_table(self.tableLoads,
                    3, 1, ["Из узла", "В узел", "Объём информации(в Байт/c)"])
        setup_table(self.tablePackagesInput,
                    1, 1, ["Размер пакета(в байтах)"])
        setup_table(self.tableChannelsInput,
                    4, 1, ["Узел 1", "Узел 2", "Пропускная способность", "Стоимость"])
        setup_table(self.tableRoutersInput,
                    3, 1, ["Модель", "Пропускная способность", "Стоимость"])

        xs = [(random.randint(-n, n), random.randint(-n, n)) for i in range(n)]
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
        for i, (x, y) in enumerate(edges):
            if i != 0:
                self.tableChannelsInput.insertRow(i)
            self.tableChannelsInput.setItem(i, 0, QtWidgets.QTableWidgetItem(str(x)))
            self.tableChannelsInput.setItem(i, 1, QtWidgets.QTableWidgetItem(str(y)))
            self.tableChannelsInput.setItem(i, 2, QtWidgets.QTableWidgetItem(rate_default))
            self.tableChannelsInput.setItem(i, 3, QtWidgets.QTableWidgetItem(price_default))

    def ready(self):
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
                        error(f"Неверный формат информации о пакетах!\n Отрицательный размер пакета! Строка {i + 1}")
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
                if j == 2:
                    if is_number(v):
                        if int(v) <= 0:
                            error(f"Отрицательный объём информации в {i + 1} строке матрицы нагрузки")
                        tmp[self.tableLoads.horizontalHeaderItem(j).text()] = int(v)
                    else:
                        error(f"Некорректный объём информации в {i + 1} строке матрицы нагрузки")
                        return
                else:
                    if v not in names_of_points:
                        error(f"Узла, указанного в {i + 1} строке матрицы нагрузки нет в списке узлов")
                        return
                    tmp[self.tableLoads.horizontalHeaderItem(j).text()] = v
            self.loads.append(tmp)

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
                else:
                    if v not in names_of_points:
                        error(f"Узла, указанного в {i + 1} строке информации о каналах нет в списке узлов")
                        return
                    tmp[self.tableChannelsInput.horizontalHeaderItem(j).text()] = v

            edge = (min(tmp["Узел 1"], tmp["Узел 2"]), max(tmp["Узел 1"], tmp["Узел 2"]))
            if edge in channels_name:
                error("Каналы не могут дублироваться!")
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
                if j > 1:
                    if is_number(v):
                        if int(v) <= 0:
                            error(f"Отрицательная {self.tableRoutersInput.horizontalHeaderItem(j).text()}"
                                  f" в {i + 1} строке доступных маршрутизаторов!")
                            return
                        tmp[self.tableRoutersInput.horizontalHeaderItem(j).text()] = v
                    else:
                        error(f"Некорректная {self.tableRoutersInput.horizontalHeaderItem(j).text()}"
                              f" в {i + 1} строке доступных маршрутизаторов!")
                else:
                    if len(v) == 0:
                        error("Название модели маршрутизатора не может быть пустым!")
                        return
                    if v in names:
                        error("Название модели маршрутизатора не может дублироваться!")
                        return
                    names.append(v)
                    tmp[self.tableLoads.horizontalHeaderItem(j).text()] = v
            self.routers.append(tmp)

        self.correct_info = True
        self.close()