import networkx as nx
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class GraphWidget(FigureCanvas):
    """Граф"""

    def __init__(self, parent=None):
        fig = plt.figure(figsize=(5, 5))
        super(GraphWidget, self).__init__(fig)
        self.ax = fig.add_subplot(111)
        self.setParent(parent)

    def plot(self, graph: nx.Graph, pos: dict, edge_labels: dict = None, node_labels: dict = None):
        """plot(graph) отображает граф graph с подписями на рёбрах и узлах"""
        self.ax.clear()

        # Отрисовка графа
        nx.draw(graph, pos, ax=self.ax, with_labels=True, node_color='skyblue',
                node_size=800, font_size=10, font_color='darkgreen', edge_color='black')

        # Добавление подписей на рёбра
        if edge_labels:
            nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, ax=self.ax,
                                         font_color='red', font_size=8)

        # Добавление дополнительных подписей для узлов
        if node_labels:
            nx.draw_networkx_labels(graph, pos, labels=node_labels, ax=self.ax,
                                    font_size=8, font_color='blue', verticalalignment='bottom')

        self.draw()