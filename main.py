import sys
import time
import json

import matplotlib.pyplot as plt
import networkx as nx
from PyQt6 import QtWidgets
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QMessageBox, QAbstractItemView
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from dialog import InputDialog
from edit_window import EditDialog
from main_window import Ui_MainWindow
from channel_ui import AddChannel


# TO-DO
# поиск путей маршрутов - допилить

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
        pos = nx.get_node_attributes(graph, 'pos')
        nx.draw(graph, pos, ax=self.ax, with_labels=True, node_color='skyblue', node_size=800, font_size=10,
                font_color='darkgreen', edge_color='gray')
        self.draw()


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


def setup_table(table: QtWidgets.QTableWidget, table_from: list):
    rows = len(table_from)
    columns = len(table_from[0].keys())
    headers = [x for x in table_from[0].keys()]

    table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)  # Отключаем редактирование для всех ячеек

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


def setup_matrix(table: QtWidgets.QTableWidget, columns: int, list_headers: list, table_from: list, points: list):
    table.setEnabled(True)
    table.setRowCount(0)
    table.setColumnCount(columns)
    table.setRowCount(columns)
    table.setHorizontalHeaderLabels(list_headers)
    table.setVerticalHeaderLabels(list_headers)

    table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

    for i in range(columns):
        table.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)

    try:
        for i in range(columns):
            for j in range(columns):
                table.setItem(i, j, QtWidgets.QTableWidgetItem(""))
                if i == j:
                    table.item(i, j).setBackground(QColor.fromRgb(100, 0, 0))

        for load in table_from:
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

    except Exception as e:
        error(str(e))


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.plotWidget.setVisible(False)
        self.graph_widget = GraphWidget(self.plotWidget)
        self.add_channel_widget = AddChannel()
        self.dialog = InputDialog()
        self.edges = []
        self.ps, self.rs, self.chs, self.pkgs, self.loads = [], [], [], [], []

        self.clearButton.clicked.connect(self.clear)
        self.inputButton.clicked.connect(self.open_input)
        self.editButton.clicked.connect(self.open_edit)

        self.addChanelButton.setVisible(False)
        self.deleteChannelButton.setVisible(False)

        self.action_save.triggered.connect(self.save_file)
        self.action_open.triggered.connect(self.open_file)

        self.addChanelButton.clicked.connect(self.add_channel)
        self.deleteChannelButton.clicked.connect(self.delete_channel)

    def show_graph(self):
        G = nx.Graph()
        # G.add_node(self.points)
        for point in self.ps:
            x, y = point['X'], point['Y']
            name = point['Имя узла']
            G.add_node(name, pos=(x, y))
        G.add_edges_from(self.edges)
        self.graph_widget.plot(G)
        self.plotWidget.setVisible(True)

    def open_edit(self):
        self.edit_dialog = EditDialog(self.ps, self.rs, self.chs, self.pkgs, self.loads)
        self.edit_dialog.exec()
        while True:
            time.sleep(0.5)
            if self.edit_dialog.finished:
                break
        to_read_info = self.edit_dialog.correct_info
        if to_read_info:
            self.clear()
            self.ps = self.edit_dialog.points
            self.rs = self.edit_dialog.routers
            self.chs = self.edit_dialog.channels
            self.pkgs = self.edit_dialog.packages
            self.loads = self.edit_dialog.loads
            self.edit_dialog.clear()
            self.addChanelButton.setVisible(True)
            self.deleteChannelButton.setVisible(True)
            self.put_info(self.ps, self.rs, self.chs, self.pkgs, self.loads)
            self.get_info(self.chs)
            self.show_graph()

    def open_input(self):
        self.dialog.exec()
        while True:
            time.sleep(0.5)
            if self.dialog.finished:
                break
        to_read_info = self.dialog.correct_info
        self.ps = self.dialog.points
        self.rs = self.dialog.routers
        self.chs = self.dialog.channels
        self.pkgs = self.dialog.packages
        self.loads = self.dialog.loads
        self.dialog.clear()
        if to_read_info:
            self.addChanelButton.setVisible(True)
            self.deleteChannelButton.setVisible(True)
            self.put_info(self.ps, self.rs, self.chs, self.pkgs, self.loads)
            self.get_info(self.chs)
            self.show_graph()

    def put_info(self, ps, rs, chs, pkgs, loads):
        setup_table(self.tablePoint, ps)
        setup_table(self.tableRouters, rs)
        setup_table(self.tableChannels, chs)
        setup_table(self.tablePackages, pkgs)
        setup_matrix(self.tableUsages, len(loads), [str(i + 1) for i in range(len(loads))], loads, self.ps)

    def build_graph(self):
        G = nx.Graph()
        # Add nodes with attributes
        for node_dict in self.ps:
            node_name = node_dict['Имя узла']
            G.add_node(node_name, X=node_dict['X'], Y=node_dict['Y'])
        # Add edges with cost as weight
        for channel in self.chs:
            node1 = channel['Узел 1']
            node2 = channel['Узел 2']
            cost_str = channel['Стоимость']
            try:
                cost = float(cost_str)
                G.add_edge(node1, node2, weight=cost)
            except ValueError:
                print(f"Invalid cost value: {cost_str} for edge {node1}-{node2}")
        return G

    def find_shortest_path_dijkstra(self, start_node, end_node):
        self.graph = self.build_graph()
        if start_node not in self.graph:
            return f"Start node '{start_node}' not in graph."
        if end_node not in self.graph:
            return f"End node '{end_node}' not in graph."
        try:
            path = nx.dijkstra_path(self.graph, source=start_node, target=end_node, weight='weight')
            cost = nx.dijkstra_path_length(self.graph, source=start_node, target=end_node, weight='weight')
            return f"Shortest path: {path} with cost: {cost}"
        except nx.NetworkXNoPath:
            return f"No path exists between '{start_node}' and '{end_node}'."

    def get_info(self, ch):
        for item in ch:
            x, y = item["Узел 1"], item["Узел 2"]
            # x_name, y_name = '', ''
            # for tmp in self.ps:
            #     if tmp['Имя узла'] == x:
            #         x_name = tmp['Номер']
            #         break
            # for tmp in self.ps:
            #     if tmp['Имя узла'] == y:
            #         y_name = tmp['Номер']
            #         break
            # x, y = min(x, y), max(x, y)
            self.edges.append([x, y])

    def clear(self):
        self.edges = []
        # self.ps, self.rs, self.chs, self.pkgs, self.loads = [], [], [], [], []
        self.graph_widget.ax.clear()
        self.plotWidget.setVisible(False)
        self.tableUsages.setRowCount(0)
        self.tableUsages.setColumnCount(0)
        self.tablePoint.setRowCount(0)
        self.tableRouters.setRowCount(0)
        self.tableChannels.setRowCount(0)
        self.tablePackages.setRowCount(0)
        self.addChanelButton.setVisible(False)
        self.deleteChannelButton.setVisible(False)

    def save_file(self):
        try:
            to_save = dict()
            to_save['Points'] = []
            for point in self.ps:
                tmp = dict()
                tmp['Name'] = point['Имя узла']
                tmp['X'] = point['X']
                tmp['Y'] = point['Y']
                tmp['ID'] = point['Номер']
                to_save['Points'].append(tmp)
            to_save['Routers'] = []
            for router in self.rs:
                tmp = dict()
                tmp['Model Name'] = router['Модель']
                tmp['Bandwidth'] = router['Пропускная способность']
                tmp['Cost'] = router['Стоимость']
                to_save['Routers'].append(tmp)
            to_save['Channels'] = []
            for chnl in self.chs:
                tmp = dict()
                tmp['Point 1'] = chnl['Узел 1']
                tmp['Point 2'] = chnl['Узел 2']
                tmp['Bandwidth'] = chnl['Пропускная способность']
                tmp['Cost'] = chnl['Стоимость']
                to_save['Channels'].append(tmp)
            to_save['Packages'] = []
            for pkg in self.pkgs:
                tmp = dict()
                tmp['Size'] = pkg['Размер пакета(в байтах)']
                to_save['Packages'].append(tmp)
            to_save['Loads'] = []
            for load in self.loads:
                tmp = dict()
                tmp['From point'] = load['Из узла']
                tmp['To point'] = load['В узел']
                tmp['Info volume'] = load['Объём информации(в Байт/c)']
                to_save['Loads'].append(tmp)

            name = QtWidgets.QFileDialog.getSaveFileName(self, 'Сохранить файл')[0]

            with open(f"{name}.json", "w") as fh:
                json.dump(to_save, fh)
            error(f"Файл успешно сохранен по адресу:\n{name}.json")
        except Exception as e:
            error(str(e))

    def open_file(self):
        file, _ = QtWidgets.QFileDialog.getOpenFileName(self,
                                                        'Open File',
                                                        './',
                                                        'Config (*.json)')
        if not file:
            error("Некорректный файл!")
            return
        try:
            with open(file, 'r') as f:
                read_from = json.load(f)

            self.clear()
            for point in read_from['Points']:
                tmp = dict()
                tmp['Имя узла'] = point['Name']
                tmp['X'] = point['X']
                tmp['Y'] = point['Y']
                tmp['Номер'] = point['ID']
                self.ps.append(tmp)
            for router in read_from['Routers']:
                tmp = dict()
                tmp['Модель'] = router['Model Name']
                tmp['Пропускная способность'] = router['Bandwidth']
                tmp['Стоимость'] = router['Cost']
                self.rs.append(tmp)
            for chnl in read_from['Channels']:
                tmp = dict()
                tmp['Узел 1'] = chnl['Point 1']
                tmp['Узел 2'] = chnl['Point 2']
                tmp['Пропускная способность'] = chnl['Bandwidth']
                tmp['Стоимость'] = chnl['Cost']
                self.chs.append(tmp)
            for pkg in read_from['Packages']:
                tmp = dict()
                tmp['Размер пакета(в байтах)'] = pkg['Size']
                self.pkgs.append(tmp)
            for load in read_from['Loads']:
                tmp = dict()
                tmp['Из узла'] = load['From point']
                tmp['В узел'] = load['To point']
                tmp['Объём информации(в Байт/c)'] = load['Info volume']
                self.loads.append(tmp)
            self.put_info(self.ps, self.rs, self.chs, self.pkgs, self.loads)
            self.get_info(self.chs)
            self.show_graph()
            self.addChanelButton.setVisible(True)
            self.deleteChannelButton.setVisible(True)

            error(self.find_shortest_path_dijkstra('Москва', 'Самара'))
        except Exception as e:
            error(f"Что-то пошло не так...\n {str(e)}")

    def add_channel(self):
        self.add_channel_widget.exec()
        while True:
            time.sleep(0.5)
            if self.add_channel_widget.finished:
                break
        to_read_info = self.add_channel_widget.correct_info
        x1, x2 = self.add_channel_widget.x1, self.add_channel_widget.x2
        bw, cst = self.add_channel_widget.bandwidth, self.add_channel_widget.cost
        self.add_channel_widget.clear()
        if to_read_info:
            try:
                # читаем данные
                new_channel = {
                    "Узел 1": x1,
                    "Узел 2": x2,
                    "Пропускная способность": bw,
                    "Стоимость": cst
                }
                tmp_points = [x['Имя узла'] for x in self.ps]
                if new_channel['Узел 1'] not in tmp_points or new_channel['Узел 2'] not in tmp_points:
                    error("Один из введенных вами узлов не существует!")
                    return
                self.chs.append(new_channel)
                self.tableChannels.setRowCount(0)
                setup_table(self.tableChannels, self.chs)
                self.edges.append([new_channel['Узел 1'], new_channel['Узел 2']])

                self.graph_widget.ax.clear()
                self.plotWidget.setVisible(False)
                self.show_graph()
            except Exception as e:
                error(str(e))

    def delete_channel(self):
        if len(self.tableChannels.selectedItems()) == 0:
            error("Чтобы удалить канал, выберите его в Таблице Каналов!")
            return
        if self.tableChannels.rowCount() == 0:
            error("Каналов нет!")
            return
        try:
            if self.tableChannels.rowCount() > 0:
                index = self.tableChannels.currentRow()
                row_to_delete = []
                for i in range(self.tableChannels.columnCount()):
                    row_to_delete.append(self.tableChannels.item(index, i).text())
                for i, j in enumerate(self.chs):
                    if j['Узел 1'] == row_to_delete[0] and j['Узел 2'] == row_to_delete[1]:
                        self.chs = self.chs[:i] + self.chs[i + 1:]
                for i, j in enumerate(self.edges):
                    if j[0] == row_to_delete[0] and j[1] == row_to_delete[1]:
                        self.edges = self.edges[:i] + self.edges[i + 1:]
                self.tableChannels.removeRow(self.tableChannels.currentRow())
                self.graph_widget.ax.clear()
                self.plotWidget.setVisible(False)
                self.show_graph()
        except Exception as e:
            error(str(e))


app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()
