import sys
import time

import matplotlib.pyplot as plt
import networkx as nx
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from dialog import InputDialog
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


def is_number(n: str):
    """is_number(n) Проверяет, является ли n числом"""
    if len(n) == 0 or (n[0] == '-' and any(x.isdigit() is False for x in n[1:])
                       or (n[0] != '-' and any(x.isdigit() is False for x in n))):
        return False
    return True


def setup_table(table: QtWidgets.QTableWidget, table_from: list):
    rows = len(table_from)
    columns = len(table_from[0].keys())
    headers = [x for x in table_from[0].keys()]

    table.setEnabled(True)
    table.setColumnCount(columns)
    table.setRowCount(rows)
    table.setHorizontalHeaderLabels(headers)
    for i in range(columns):
        (table.horizontalHeader().
         setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents))
    table.horizontalHeader().setStretchLastSection(True)

    try:
        for i in range(rows):
            for j, h in enumerate(headers):
                table.setItem(i, j, QtWidgets.QTableWidgetItem(str(table_from[i][h])))
    except Exception as e:
        error(str(e))


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.plotWidget.setVisible(False)
        self.graph_widget = GraphWidget(self.plotWidget)
        self.dialog = InputDialog()
        self.edges = []

        self.addChanelButton.clicked.connect(self.show_graph)
        self.inputButton.clicked.connect(self.open_input)

    def show_graph(self):
        G = nx.Graph()
        G.add_edges_from(self.edges)
        self.graph_widget.plot(G)
        self.plotWidget.setVisible(True)

    def open_input(self):
        self.dialog.exec()
        while True:
            time.sleep(0.5)
            if self.dialog.finished:
                break
        if self.dialog.correct_info:
            self.put_info()
            self.get_info()

    def put_info(self):
        setup_table(self.tablePoint, self.dialog.points)
        setup_table(self.tableRouters, self.dialog.routers)
        setup_table(self.tableChannels, self.dialog.channels)
        setup_table(self.tablePackages, self.dialog.packages)
        setup_table(self.tableUsages, self.dialog.loads)

    def get_info(self):
        for item in self.dialog.channels:
            x, y = item["Узел 1"], item["Узел 2"]
            x, y = min(x, y), max(x, y)
            self.edges.append([x, y])


app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()
