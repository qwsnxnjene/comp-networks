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
            table.setItem(fr - 1, to - 1, QtWidgets.QTableWidgetItem(str(load['Объём информации(в Бит/c)'])))
            table.setItem(to - 1, fr - 1, QtWidgets.QTableWidgetItem(str(load['Объём информации(в Бит/c)'])))

    for i in range(columns):
        for j in range(columns):
            if i != j and table.item(i, j).text() == "":
                table.setItem(i, j, QtWidgets.QTableWidgetItem("-"))


def setup_channels_matrix(table: QtWidgets.QTableWidget, columns: int, list_headers: list, info_from: list,
                          points: list):
    """
    Настраивает таблицу для отображения матрицы каналов.

    :param table: Таблица для настройки.
    :param columns: Количество столбцов/строк.
    :param list_headers: Заголовки столбцов/строк.
    :param info_from: Данные для заполнения таблицы (список каналов).
    :param points: Список узлов (для определения номеров узлов).
    """
    try:
        table.setEnabled(True)
        table.setRowCount(0)
        table.setColumnCount(columns)
        table.setRowCount(columns)
        table.setHorizontalHeaderLabels(list_headers)
        table.setVerticalHeaderLabels(list_headers)

        # Настройка таблицы
        for i in range(columns):
            table.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
            for j in range(columns):
                table.setItem(i, j, QtWidgets.QTableWidgetItem("0"))  # По умолчанию заполняем "0"
                if i == j:
                    table.setItem(i, j, QtWidgets.QTableWidgetItem(""))  # Диагональные ячейки
                    table.item(i, j).setBackground(QColor.fromRgb(100, 0, 0))  # Выделяем цветом

        # Заполнение таблицы данными
        for channel in info_from:
            fr, to = -999, -999
            for point in points:
                if point['Имя узла'] == channel['Из узла']:
                    fr = int(point['Номер'])
                if point['Имя узла'] == channel['В узел']:
                    to = int(point['Номер'])
                if fr != -999 and to != -999:
                    break

            if fr != -999 and to != -999:
                # Устанавливаем значение связи (0 или 1)
                value = str(channel['Связь'])
                table.setItem(fr - 1, to - 1, QtWidgets.QTableWidgetItem(value))
                table.setItem(to - 1, fr - 1, QtWidgets.QTableWidgetItem(value))  # Симметричное заполнение
    except Exception as e:
        error(str(e))


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
        self.tableChannels.setRowCount(0)

        self.points = points
        self.packages = packages
        self.loads = loads
        self.channels = channels
        self.routers = routers
        self.correct_info = False

        self.tableLoads.cellChanged.connect(self.on_cell_changed)
        self.tableChannels.cellChanged.connect(self.on_channel_cell_changed)

        setup_table(self.tablePointInput, self.points, 3, len(self.points), ["Имя узла", "X", "Y"])
        setup_matrix(self.tableLoads, len(self.points), [str(i + 1) for i in range(len(self.points))],
                     self.loads, self.points)
        setup_channels_matrix(self.tableChannels, len(self.points),
                              [str(i + 1) for i in range(len(self.points))], self.channels, self.points)

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

    def on_channel_cell_changed(self, row, col):
        # Получаем значение из измененной ячейки
        item = self.tableChannels.item(row, col)
        if item:
            value = item.text()

            # # Проверяем, что введено 0 или 1
            # if value not in {"0", "1", ""}:
            #     error("Введите только 0 или 1!")
            #     item.setText("0")  # Сбрасываем значение на 0
            #     return

            # Устанавливаем симметричное значение
            symmetric_item = self.tableChannels.item(col, row)
            if not symmetric_item:
                symmetric_item = QTableWidgetItem()
                self.tableChannels.setItem(col, row, symmetric_item)
            symmetric_item.setText(value)

            # Блокируем сигналы, чтобы избежать рекурсии
            self.tableChannels.blockSignals(True)
            symmetric_item.setText(value)
            self.tableChannels.blockSignals(False)

    def ready(self):
        try:
            names_of_points = []

            self.points = []
            self.loads = []
            self.channels = []

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
                for j in range(i + 1, column_count):
                    v = self.tableLoads.item(i, j).text()
                    if is_number(v):
                        if int(v) < 0:
                            error(f"Отрицательный объём информации в {i + 1} строке {j + 1} столбце матрицы нагрузки")
                            return
                        tmp['Из узла'] = [point['Имя узла'] for point in self.points if point['Номер'] == str(i + 1)][0]
                        tmp['В узел'] = [point['Имя узла'] for point in self.points if point['Номер'] == str(j + 1)][0]
                        tmp['Объём информации(в Бит/c)'] = int(v)
                    elif v == '':
                        continue
                    else:
                        error(f"Некорректный объём информации в {i + 1} строке {j + 1} столбце матрицы нагрузки")
                        return
                    self.loads.append(tmp)
                    tmp = dict()

            row_count = self.tableChannels.rowCount()
            column_count = self.tableChannels.columnCount()
            for i in range(row_count):
                for j in range(i + 1, column_count):  # Обрабатываем только верхний треугольник матрицы
                    v = self.tableChannels.item(i, j).text()
                    if v == "1":  # Добавляем только каналы с связью
                        tmp = {
                            'Из узла': [point['Имя узла'] for point in self.points if point['Номер'] == str(i + 1)][0],
                            'В узел': [point['Имя узла'] for point in self.points if point['Номер'] == str(j + 1)][0],
                            'Связь': int(v)
                        }
                        self.channels.append(tmp)
                    elif v not in {"0", ""}:  # Проверяем, что введено допустимое значение
                        error(f"Некорректное значение связи в {i + 1} строке {j + 1} столбце матрицы каналов")
                        return
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
