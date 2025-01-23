import networkx as nx
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMessageBox

from shortest_path import Ui_ShortestPathDialog


def error(message: str):
    """error(message) выводит сообщение message в появляющемся окне"""
    msgBox = QMessageBox()
    msgBox.setWindowTitle("Внимание!")
    # message = message.split(':')[1][1:].capitalize()
    msgBox.setText(message)
    msgBox.exec()


class ShortestDialog(QtWidgets.QDialog, Ui_ShortestPathDialog):
    """Окно ввода входных данных"""

    def __init__(self, points, channels):
        super(ShortestDialog, self).__init__()
        self.graph = None
        self.setupUi(self)

        self.points = points
        self.channels = channels
        self.fromChoice.addItems([x['Имя узла'] for x in self.points])
        self.toChoice.addItems([x['Имя узла'] for x in self.points])

        self.findButton.clicked.connect(self.find_shortest)

    def find_shortest(self):
        error(self.find_shortest_dijkstra())

    def find_shortest_dijkstra(self):
        start_node, end_node = self.fromChoice.currentText(), self.toChoice.currentText()
        self.graph = self.build_graph()
        if start_node not in self.graph:
            return f"Начальный узел '{start_node}' не найден."
        if end_node not in self.graph:
            return f"Конечный узел '{end_node}' не найден."
        try:
            path = nx.dijkstra_path(self.graph, source=start_node, target=end_node, weight='weight')
            cost = nx.dijkstra_path_length(self.graph, source=start_node, target=end_node, weight='weight')
            return (f"Кратчайший путь из узла"
                    f" {repr(start_node)} в узел {repr(end_node)}: {"->".join(path)} со стоимостью: {cost}")
        except nx.NetworkXNoPath:
            return f"Не найдено пути между '{start_node}' и '{end_node}'."

    def build_graph(self):
        G = nx.Graph()
        # добавляем в граф узлы
        for node_dict in self.points:
            node_name = node_dict['Имя узла']
            G.add_node(node_name, X=node_dict['X'], Y=node_dict['Y'])
        # добавляем ребра, со стоимостью как вес ребра
        for channel in self.channels:
            node1 = channel['Узел 1']
            node2 = channel['Узел 2']
            cost_str = channel['Стоимость']
            try:
                cost = float(cost_str)
                G.add_edge(node1, node2, weight=cost)
            except ValueError:
                print(f"Invalid cost value: {cost_str} for edge {node1}-{node2}")
        return G
