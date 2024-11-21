import sys
from PyQt6 import QtWidgets
from MainWindow import Ui_MainWindow
from inputWindow import Ui_DialogAdd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import networkx as nx


class GraphWidget(FigureCanvas):
    def __init__(self, parent=None):
        fig = plt.figure(figsize=(7, 7))
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
        G.add_edges_from([(1, 2), (1, 3), (2, 4), (3, 4)])
        self.graph_widget.plot(G)
        self.plotWidget.setVisible(True)

    def open_input(self):
        input_dialog = InputDialog()
        input_dialog.exec()


app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()