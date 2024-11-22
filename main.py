import random
import sys

import matplotlib.pyplot as plt
import networkx as nx
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from input_window import Ui_DialogAdd
from main_window import Ui_MainWindow


class GraphWidget(FigureCanvas):
    """Граф"""

    def __init__(self, parent=None):
        fig = plt.figure(figsize=(5, 5))
        super(GraphWidget, self).__init__(fig)
        self.ax = fig.add_subplot(111)
        self.setParent(parent)

    def plot(self, graph: nx.Graph):
        """plot(graph) отображает граф graph"""
        self.ax.clear()
        pos = nx.circular_layout(graph)
        nx.draw(graph, pos, ax=self.ax, with_labels=True, node_color='skyblue', node_size=800, font_size=10,
                font_color='darkgreen', edge_color='gray')
        self.draw()


def error(message: str):
    """error(message) выводит сообщение message в появляющемся окне"""
    msgBox = QMessageBox()
    msgBox.setWindowTitle("Внимание!")
    message = message.split(':')[1][1:].capitalize()
    msgBox.setText(message)
    msgBox.exec()


def is_number(n: int):
    """is_number(n) Проверяет, является ли n числом"""
    if len(n) == 0 or (n[0] == '-' and any(x.isdigit() is False for x in n[1:])
                       or (n[0] != '-' and any(x.isdigit() is False for x in n))):
        return False
    return True


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


class InputDialog(QtWidgets.QDialog, Ui_DialogAdd):
    """Окно ввода входных данных"""
    def __init__(self):
        super(InputDialog, self).__init__()
        self.setupUi(self)
        self.createButton.clicked.connect(self.manualCreate)

        self.points = []
        self.edges = []

        # реализация Добавления, удаления и копирования в таблицах для входных данных
        self.addButtonLoads.clicked.connect(self.add_load)
        self.deleteButtonLoads.clicked.connect(self.rm_load)
        self.copyButtonLoads.clicked.connect(self.cp_load)

        self.addButtonPackages.clicked.connect(self.add_package)
        self.deleteButtonPackages.clicked.connect(self.rm_package)
        self.copyButtonPackages.clicked.connect(self.cp_package)

        self.addButtonChannels.clicked.connect(self.add_channel)
        self.deleteButtonChannels.clicked.connect(self.rm_channel)
        self.copyButtonChannels.clicked.connect(self.cp_channel)

        self.addButtonRouters.clicked.connect(self.add_router)
        self.deleteButtonRouters.clicked.connect(self.rm_router)
        self.copyButtonRouters.clicked.connect(self.cp_router)

    def manualCreate(self):
        """Ручное добавление данных"""
        n = self.inputNumOfPoints.text()
        if not is_number(n):
            # print("[manualCreate]: введёно не число")
            error("[manualCreate]: введёно не число")
            return
        n = int(n)
        if n <= 0:
            # print("[manualCreate]: число узлов не может быть меньше или равно нулю!")
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

    def add_load(self):
        self.tableLoads.insertRow(self.tableLoads.currentRow() + 1)

    def rm_load(self):
        if self.tableLoads.rowCount() > 0:
            self.tableLoads.removeRow(self.tableLoads.currentRow())

    def cp_load(self):
        self.tableLoads.insertRow(self.tableLoads.rowCount())
        row_count = self.tableLoads.rowCount()
        column_count = self.tableLoads.columnCount()

        for j in range(column_count):
            if not self.tableLoads.item(row_count - 2, j) is None:
                self.tableLoads.setItem(row_count - 1, j,
                                        QtWidgets.QTableWidgetItem(self.tableLoads.item(row_count - 2, j).text()))

    def add_package(self):
        self.tablePackagesInput.insertRow(self.tablePackagesInput.currentRow() + 1)

    def rm_package(self):
        if self.tablePackagesInput.rowCount() > 0:
            self.tablePackagesInput.removeRow(self.tablePackagesInput.currentRow())

    def cp_package(self):
        self.tablePackagesInput.insertRow(self.tablePackagesInput.rowCount())
        row_count = self.tablePackagesInput.rowCount()
        column_count = self.tablePackagesInput.columnCount()

        for j in range(column_count):
            if not self.tablePackagesInput.item(row_count - 2, j) is None:
                self.tablePackagesInput.setItem(row_count - 1, j,
                                                QtWidgets.QTableWidgetItem(
                                                    self.tablePackagesInput.item(row_count - 2, j).text()))

    def add_channel(self):
        self.tableChannelsInput.insertRow(self.tableChannelsInput.currentRow() + 1)

    def rm_channel(self):
        if self.tableChannelsInput.rowCount() > 0:
            self.tableChannelsInput.removeRow(self.tableChannelsInput.currentRow())

    def cp_channel(self):
        self.tableChannelsInput.insertRow(self.tableChannelsInput.rowCount())
        row_count = self.tableChannelsInput.rowCount()
        column_count = self.tableChannelsInput.columnCount()

        for j in range(column_count):
            if not self.tableChannelsInput.item(row_count - 2, j) is None:
                self.tableChannelsInput.setItem(row_count - 1, j,
                                                QtWidgets.QTableWidgetItem(
                                                    self.tableChannelsInput.item(row_count - 2, j).text()))

    def add_router(self):
        self.tableRoutersInput.insertRow(self.tableRoutersInput.currentRow() + 1)

    def rm_router(self):
        if self.tableRoutersInput.rowCount() > 0:
            self.tableRoutersInput.removeRow(self.tableRoutersInput.currentRow())

    def cp_router(self):
        self.tableRoutersInput.insertRow(self.tableRoutersInput.rowCount())
        row_count = self.tableRoutersInput.rowCount()
        column_count = self.tableRoutersInput.columnCount()

        for j in range(column_count):
            if not self.tableRoutersInput.item(row_count - 2, j) is None:
                self.tableRoutersInput.setItem(row_count - 1, j,
                                               QtWidgets.QTableWidgetItem(
                                                   self.tableRoutersInput.item(row_count - 2, j).text()))

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
            edges.append((i, i + 1))

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

        self.points, self.edges = xs, edges


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.plotWidget.setVisible(False)
        self.graph_widget = GraphWidget(self.plotWidget)
        self.dialog = InputDialog()

        self.addChanelButton.clicked.connect(self.show_graph)
        self.inputButton.clicked.connect(self.open_input)

    def show_graph(self):
        G = nx.Graph()
        G.add_edges_from(self.dialog.edges)
        self.graph_widget.plot(G)
        self.plotWidget.setVisible(True)

    def open_input(self):
        self.dialog.exec()


app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()
