import sys
from PyQt6 import QtWidgets

from main_window import Ui_MainWindow
from input_window import Ui_DialogAdd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import networkx as nx


class GraphWidget(FigureCanvas):
    def __init__(self, parent=None):
        fig = plt.figure(figsize=(5, 5))
        super(GraphWidget, self).__init__(fig)
        self.ax = fig.add_subplot(111)
        self.setParent(parent)

    def plot(self, graph):
        self.ax.clear()
        pos = nx.circular_layout(graph)
        nx.draw(graph, pos, ax=self.ax, with_labels=True, node_color='skyblue', node_size=800, font_size=10,
                font_color='darkgreen', edge_color='gray')
        self.draw()


class InputDialog(QtWidgets.QDialog, Ui_DialogAdd):
    def __init__(self):
        super(InputDialog, self).__init__()
        self.setupUi(self)
        self.createButton.clicked.connect(self.manualCreate)

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
        n = self.inputNumOfPoints.text()
        if sum(n.count(x) for x in '0123456789') != len(n) or len(n) == 0:
            print("[manualCreate]: not a number")
            return
        n = int(n)
        if n <= 0:
            print("[manualCreate]: number of nodes can't be negative or zero")
            return
        if self.checkAuto.isChecked():
            self.autoCreate()
            return

        self.tablePointInput.setEnabled(True)
        self.tablePointInput.setColumnCount(3)
        self.tablePointInput.setRowCount(n)
        self.tablePointInput.setHorizontalHeaderLabels(["Имя узла", "X", "Y"])
        for i in range(3):
            (self.tablePointInput.horizontalHeader().
             setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents))
        self.tablePointInput.horizontalHeader().setStretchLastSection(True)

        self.tableLoads.setEnabled(True)
        self.tableLoads.setColumnCount(3)
        self.tableLoads.setRowCount(1)
        self.tableLoads.setHorizontalHeaderLabels(["Из узла", "В узел", "Объём информации(в Бит/c)"])
        for i in range(3):
            (self.tableLoads.horizontalHeader().
             setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents))
        self.tableLoads.horizontalHeader().setStretchLastSection(True)

        self.tablePackagesInput.setEnabled(True)
        self.tablePackagesInput.setColumnCount(1)
        self.tablePackagesInput.setRowCount(1)
        (self.tablePackagesInput.horizontalHeader().
         setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents))
        self.tablePackagesInput.setHorizontalHeaderLabels(["Размер пакета(в битах)"])

        self.tablePackagesInput.horizontalHeader().setStretchLastSection(True)

        self.tableChannelsInput.setEnabled(True)
        self.tableChannelsInput.setColumnCount(4)
        self.tableChannelsInput.setRowCount(1)
        self.tableChannelsInput.setHorizontalHeaderLabels(["Узел 1", "Узел 2", "Пропускная способность", "Стоимость"])
        for i in range(4):
            (self.tableChannelsInput.horizontalHeader().
             setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents))
        self.tableChannelsInput.horizontalHeader().setStretchLastSection(True)

        self.tableRoutersInput.setEnabled(True)
        self.tableRoutersInput.setColumnCount(3)
        self.tableRoutersInput.setRowCount(1)
        self.tableRoutersInput.setHorizontalHeaderLabels(["Модель", "Пропускная способность", "Стоимость"])
        for i in range(3):
            (self.tableRoutersInput.horizontalHeader().
             setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents))
        self.tableRoutersInput.horizontalHeader().setStretchLastSection(True)

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

    def autoCreate(self):
        pass


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.plotWidget.setVisible(False)
        self.graph_widget = GraphWidget(self.plotWidget)

        self.addChanelButton.clicked.connect(self.show_graph)
        self.inputButton.clicked.connect(self.open_input)

    def show_graph(self):
        G = nx.Graph()
        G.add_edges_from([(1, 2), (1, 3), (2, 4), (3, 4), (5, 1)])
        self.graph_widget.plot(G)
        self.plotWidget.setVisible(True)

    def open_input(self):
        input_dialog = InputDialog()
        input_dialog.exec()


app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()
