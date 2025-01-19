import networkx as nx
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QTabWidget, QVBoxLayout, QWidget, QComboBox, QLabel, QTableWidget, QTableWidgetItem
from graph_class import GraphWidget


class ConfigurationViewer(QtWidgets.QDialog):
    def __init__(self, config_min_cost, config_min_delay, config_optimal, packet_sizes, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Конфигурации сети")
        self.setGeometry(100, 100, 800, 600)

        self.config_min_cost = config_min_cost
        self.config_min_delay = config_min_delay
        self.config_optimal = config_optimal
        self.packet_sizes = packet_sizes

        # Создаём вкладки
        self.tabs = QTabWidget()
        self.tab_min_cost = QWidget()
        self.tab_min_delay = QWidget()
        self.tab_optimal = QWidget()

        # Добавляем вкладки
        self.tabs.addTab(self.tab_min_cost, "Минимальная стоимость")
        self.tabs.addTab(self.tab_min_delay, "Минимальная задержка")
        self.tabs.addTab(self.tab_optimal, "Оптимальная конфигурация")

        # Настраиваем вкладки
        self.setup_tab(self.tab_min_cost, self.config_min_cost)
        self.setup_tab(self.tab_min_delay, self.config_min_delay)
        self.setup_tab(self.tab_optimal, self.config_optimal)

        # Основной layout
        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def setup_tab(self, tab, config):
        """
        Настраивает вкладку с информацией о конфигурации.
        """
        layout = QVBoxLayout()

        # Выбор размера пакета
        self.packet_size_label = QLabel("Размер пакета:")
        self.packet_size_combo = QComboBox()
        for pkg in self.packet_sizes:
            self.packet_size_combo.addItem(pkg['Размер пакета'])
        self.packet_size_combo.currentIndexChanged.connect(
            lambda: self.update_delay(tab, config)
        )

        # Таблица с каналами и маршрутизаторами
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Тип", "Имя", "Параметры"])

        # Граф для визуализации
        self.graph_widget = GraphWidget()

        # Добавляем элементы на вкладку
        layout.addWidget(self.packet_size_label)
        layout.addWidget(self.packet_size_combo)
        layout.addWidget(self.table)
        layout.addWidget(self.graph_widget)

        tab.setLayout(layout)
        self.update_tab(tab, config)

    def update_tab(self, tab, config):
        """
        Обновляет информацию на вкладке.
        """
        # Очищаем таблицу
        self.table.setRowCount(0)

        # Добавляем каналы
        for edge, channel in config['channels'].items():
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem("Канал"))
            self.table.setItem(row_position, 1, QTableWidgetItem(f"{edge[0]} - {edge[1]}"))
            self.table.setItem(row_position, 2, QTableWidgetItem(
                f"Пропускная способность: {channel['Пропускная способность']}, "
                f"Стоимость: {channel['Стоимость аренды']}"
            ))

        # Добавляем маршрутизаторы
        for node, router in config['routers'].items():
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem("Маршрутизатор"))
            self.table.setItem(row_position, 1, QTableWidgetItem(node))
            self.table.setItem(row_position, 2, QTableWidgetItem(
                f"Пропускная способность: {router['Пропускная способность']}, "
                f"Стоимость: {router['Стоимость']}"
            ))

        # Обновляем граф
        self.update_graph(tab, config)

    def update_graph(self, tab, config):
        """
        Обновляет граф на вкладке.
        """
        G = nx.Graph()

        # Добавляем узлы
        for node in config['routers'].keys():
            G.add_node(node)

        # Добавляем рёбра
        for edge in config['channels'].keys():
            G.add_edge(edge[0], edge[1])

        # Отрисовываем граф
        pos = nx.spring_layout(G)
        edge_labels = {edge: config['channels'][edge]['Пропускная способность'] for edge in config['channels']}
        node_labels = {node: config['routers'][node]['Пропускная способность'] for node in config['routers']}

        self.graph_widget.plot(G, pos, edge_labels, node_labels)

    def update_delay(self, tab, config):
        """
        Обновляет задержку при изменении размера пакета.
        """
        packet_size = int(self.packet_size_combo.currentText().split()[0])  # Получаем размер пакета
        config['average_delay'] = self.calculate_delay(config, packet_size)
        self.update_tab(tab, config)

    def calculate_delay(self, config, packet_size):
        """
        Вычисляет задержку для конфигурации.
        """
        total_delay = 0
        for edge, channel in config['channels'].items():
            bandwidth = int(channel['Пропускная способность'].split()[0])
            flow = 0  # Здесь нужно получить поток для ребра (пока заглушка)
            if bandwidth > flow:
                total_delay += packet_size / (bandwidth - flow)
        return total_delay / len(config['channels']) if config['channels'] else 0