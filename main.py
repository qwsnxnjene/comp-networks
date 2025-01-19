import math
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
from collections import deque


def choose_least_loaded_path(graph, start, end, channel_flows):
    """
    Выбирает наименее загруженный кратчайший путь между start и end.
    """
    shortest_paths = find_shortest_paths(graph, start, end)
    if not shortest_paths:
        return None

    # Выбираем путь с минимальной суммарной загрузкой
    min_load = float('inf')
    best_path = None

    for path in shortest_paths:
        total_load = 0
        for i in range(len(path) - 1):
            node1, node2 = path[i], path[i + 1]
            edge = tuple(sorted([node1, node2]))
            total_load += channel_flows.get(edge, 0)

        if total_load < min_load:
            min_load = total_load
            best_path = path

    return best_path


def find_shortest_paths(graph, start, end):
    """
    Находит все кратчайшие пути между start и end в графе graph.
    """
    queue = deque([(start, [start])])
    shortest_paths = []
    shortest_length = None

    while queue:
        current_node, path = queue.popleft()
        if current_node == end:
            if shortest_length is None:
                shortest_length = len(path)
            if len(path) == shortest_length:
                shortest_paths.append(path)
            continue

        for neighbor in graph.neighbors(current_node):
            if neighbor not in path:
                queue.append((neighbor, path + [neighbor]))

    return shortest_paths


def calculate_node_flows(graph, channel_flows):
    """
    Вычисляет сумму потоков, проходящих через каждый узел.
    """
    node_flows = {node: 0 for node in graph.nodes}  # Инициализируем словарь

    for edge, flow in channel_flows.items():
        node1, node2 = edge
        node_flows[node1] += flow
        node_flows[node2] += flow

    return node_flows


def calculate_channel_flows(graph, loads):
    """
    Рассчитывает поток для каждого канала, выбирая один кратчайший путь.
    """
    channel_flows = {}  # Словарь: (узел1, узел2) -> сумма потоков

    for load in loads:
        start = load['Из узла']
        end = load['В узел']
        flow = load['Объём информации(в Бит/c)']

        # Выбираем наименее загруженный кратчайший путь
        path = choose_least_loaded_path(graph, start, end, channel_flows)
        if not path:
            continue  # Если путь не найден, пропускаем

        # Увеличиваем загрузку каналов на выбранном пути
        for i in range(len(path) - 1):
            node1, node2 = path[i], path[i + 1]
            edge = tuple(sorted([node1, node2]))  # Упорядочиваем рёбра для уникальности
            if edge not in channel_flows:
                channel_flows[edge] = 0
            channel_flows[edge] += flow

    return channel_flows


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


def error(message: str):
    """error(message) выводит сообщение message в появляющемся окне"""
    msgBox = QMessageBox()
    msgBox.setWindowTitle("Внимание!")
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
                table.setItem(fr - 1, to - 1, QtWidgets.QTableWidgetItem(str(load['Объём информации(в Бит/c)'])))
                table.setItem(to - 1, fr - 1, QtWidgets.QTableWidgetItem(str(load['Объём информации(в Бит/c)'])))

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

        self.dialog = InputDialog()
        self.edges = []
        self.ps, self.loads, self.channels = [], [], []
        self.rs = [
            {'Модель': 'TP-Link Archer C7', 'Стоимость': '5000 рублей', 'Пропускная способность': '800 бит/c'},
            {'Модель': 'Asus RT-AC88U', 'Стоимость': '15000 рублей', 'Пропускная способность': '2000 бит/c'},
            {'Модель': 'Xiaomi Mi Router 4A', 'Стоимость': '2500 рублей', 'Пропускная способность': '677 бит/c'},
            {'Модель': 'Netgear Nighthawk R7000', 'Стоимость': '12000 рублей', 'Пропускная способность': '1300 бит/c'},
            {'Модель': 'Huawei WS5200', 'Стоимость': '3500 рублей', 'Пропускная способность': '899 бит/c'},
            {'Модель': 'Cisco XYZ', 'Стоимость': '30000 рублей', 'Пропускная способность': '5000 бит/c'},
            # Новый маршрутизатор
        ]
        setup_table(self.tableRouters, self.rs)
        self.chs = [
            {'Канал': 'Ethernet 100 бит/с', 'Пропускная способность': '100 бит/c',
             'Стоимость аренды': '2000 рублей/месяц'},
            {'Канал': 'Ethernet 200 бит/с', 'Пропускная способность': '200 бит/c',
             'Стоимость аренды': '4500 рублей/месяц'},
            {'Канал': 'Ethernet 700 бит/с', 'Пропускная способность': '700 бит/c',
             'Стоимость аренды': '12000 рублей/месяц'},
            {'Канал': 'Оптоволокно 500 бит/с', 'Пропускная способность': '500 бит/c',
             'Стоимость аренды': '10000 рублей/месяц'},
            {'Канал': 'DSL 50 бит/с', 'Пропускная способность': '50 бит/c', 'Стоимость аренды': '1500 рублей/месяц'},
            {'Канал': 'Оптоволокно 1000 бит/с', 'Пропускная способность': '1000 бит/c',
             'Стоимость аренды': '20000 рублей/месяц'},  # Новый канал
        ]
        setup_table(self.tableChannels, self.chs)
        self.pkgs = [
            {'Размер пакета': '16 бит'},
            {'Размер пакета': '64 бит'},
            {'Размер пакета': '128 бит'},  # Увеличили размер пакета
            {'Размер пакета': '256 бит'}  # Увеличили размер пакета
        ]
        setup_table(self.tablePackages, self.pkgs)

        self.clearButton.clicked.connect(self.clear)
        self.inputButton.clicked.connect(self.open_input)
        self.editButton.clicked.connect(self.open_edit)

        self.action_save.triggered.connect(self.save_file)
        self.action_open.triggered.connect(self.open_file)

    def show_graph(self):
        G = nx.Graph()

        # Добавляем узлы
        for point in self.ps:
            name = point['Имя узла']
            G.add_node(name)

        # Добавляем рёбра только для каналов с наличием связи
        for channel in self.channels:
            if channel['Связь'] == 1:
                G.add_edge(channel['Из узла'], channel['В узел'])

        # Рассчитываем потоки для каналов
        channel_flows = calculate_channel_flows(G, self.loads)

        # Рассчитываем потоки для узлов
        node_flows = calculate_node_flows(G, channel_flows)

        # Конфигурация с минимальной задержкой
        min_delay_config = self.find_min_delay_configuration(channel_flows, node_flows)
        print("Конфигурация с минимальной задержкой:")
        print(f"Каналы: {min_delay_config['channels']}")
        print(f"Маршрутизаторы: {min_delay_config['routers']}")
        if min_delay_config['average_delay'] == float('inf'):
            print("Средняя задержка: Канал перегружен")
        else:
            print(f"Средняя задержка: {min_delay_config['average_delay']:.6f} секунд")
        print(f"Общая стоимость: {min_delay_config['total_cost']} рублей/месяц")

        # Конфигурация с минимальной стоимостью
        min_cost_config = self.find_min_cost_configuration(channel_flows, node_flows)
        print("\nКонфигурация с минимальной стоимостью:")
        print(f"Каналы: {min_cost_config['channels']}")
        print(f"Маршрутизаторы: {min_cost_config['routers']}")
        if min_cost_config['average_delay'] == float('inf'):
            print("Средняя задержка: Канал перегружен")
        else:
            print(f"Средняя задержка: {min_cost_config['average_delay']:.6f} секунд")
        print(f"Общая стоимость: {min_cost_config['total_cost']} рублей/месяц")

        optimal_config = self.find_optimal_configuration(channel_flows, node_flows, packet_size=16, alpha=0.5)

        if optimal_config:
            print("Оптимальная конфигурация:")
            print(f"Каналы: {optimal_config['channels']}")
            print(f"Маршрутизаторы: {optimal_config['routers']}")
            print(f"Средняя задержка: {optimal_config['average_delay']:.6f} секунд")
            print(f"Общая стоимость: {optimal_config['total_cost']} рублей/месяц")
        else:
            print("Оптимальная конфигурация не найдена.")

        # Преобразуем потоки в формат для отображения
        edge_labels = {edge: f"{flow:.2f} бит/с" for edge, flow in channel_flows.items()}

        # Преобразуем потоки в формат для отображения
        node_labels = {node: f"{flow:.2f} бит/с" for node, flow in node_flows.items()}

        # Автоматическая расстановка узлов
        pos = nx.spring_layout(G)

        # Отрисовываем граф с подписями
        self.graph_widget.plot(G, pos, edge_labels, node_labels)
        self.plotWidget.setVisible(True)

    def open_edit(self):
        self.edit_dialog = EditDialog(self.ps, self.rs, self.channels, self.pkgs, self.loads)
        self.edit_dialog.exec()
        while True:
            time.sleep(0.5)
            if self.edit_dialog.finished:
                break
        to_read_info = self.edit_dialog.correct_info
        if to_read_info:
            self.clear()
            self.ps = self.edit_dialog.points
            self.loads = self.edit_dialog.loads
            self.edit_dialog.clear()
            self.put_info(self.ps, self.loads)
            self.get_info(self.loads)
            self.show_graph()

    def open_input(self):
        self.dialog.exec()
        while True:
            time.sleep(0.5)
            if self.dialog.finished:
                break
        to_read_info = self.dialog.correct_info
        if to_read_info:
            self.clear()
            self.ps = self.dialog.points
            self.loads = self.dialog.loads
            self.channels = self.dialog.channels  # Читаем информацию о каналах
            self.dialog.clear()
            self.put_info(self.ps, self.loads)  # Передаём каналы в put_info
            self.show_graph()

    def put_info(self, ps, loads):
        setup_table(self.tablePoint, ps)
        setup_matrix(self.tableUsages, len(loads) // 2, [str(i + 1) for i in range(len(loads) // 2)], loads, self.ps)

    def get_info(self, load):
        for item in load:
            x, y = item["Из узла"], item["В узел"]
            self.edges.append([x, y])

    def clear(self):
        self.edges = []
        # self.ps, self.rs, self.chs, self.pkgs, self.loads = [], [], [], [], []
        self.graph_widget.ax.clear()
        self.plotWidget.setVisible(False)
        self.tableUsages.setRowCount(0)
        self.tableUsages.setColumnCount(0)
        self.tablePoint.setRowCount(0)

    def save_file(self):
        try:
            to_save = {
                'points': [],  # Узлы
                'loads': [],  # Матрица нагрузки
                'channels': []  # Матрица каналов
            }

            # Сохраняем узлы
            for point in self.ps:
                tmp = {
                    'Имя узла': point['Имя узла'],
                    'X': point['X'],
                    'Y': point['Y'],
                    'Номер': point['Номер']
                }
                to_save['points'].append(tmp)

            # Сохраняем матрицу нагрузки
            for load in self.loads:
                tmp = {
                    'Из узла': load['Из узла'],
                    'В узел': load['В узел'],
                    'Объём информации(в Бит/c)': load['Объём информации(в Бит/c)']
                }
                to_save['loads'].append(tmp)

            # Сохраняем матрицу каналов
            for channel in self.channels:
                tmp = {
                    'Из узла': channel['Из узла'],
                    'В узел': channel['В узел'],
                    'Связь': channel['Связь']
                }
                to_save['channels'].append(tmp)

            # Сохраняем в файл
            name = QtWidgets.QFileDialog.getSaveFileName(self, 'Сохранить файл')[0]
            if not name:
                error("Не указано имя файла!")
                return

            with open(f"{name}.json", "w", encoding="utf-8") as fh:
                json.dump(to_save, fh, ensure_ascii=False, indent=4)

            error(f"Файл успешно сохранён по адресу:\n{name}.json")
        except Exception as e:
            error(f"Ошибка при сохранении файла: {str(e)}")

    def open_file(self):
        file, _ = QtWidgets.QFileDialog.getOpenFileName(self,
                                                        'Открыть файл',
                                                        './',
                                                        'Config (*.json)')
        if not file:
            error("Файл не выбран!")
            return

        try:
            with open(file, 'r', encoding="utf-8") as f:
                data = json.load(f)

            # Очищаем текущие данные
            self.clear()

            # Загружаем узлы
            if 'points' in data:
                for point in data['points']:
                    tmp = {
                        'Имя узла': point['Имя узла'],
                        'X': point['X'],
                        'Y': point['Y'],
                        'Номер': point['Номер']
                    }
                    self.ps.append(tmp)

            # Загружаем матрицу нагрузки
            if 'loads' in data:
                for load in data['loads']:
                    tmp = {
                        'Из узла': load['Из узла'],
                        'В узел': load['В узел'],
                        'Объём информации(в Бит/c)': load['Объём информации(в Бит/c)']
                    }
                    self.loads.append(tmp)

            # Загружаем матрицу каналов
            if 'channels' in data:
                for channel in data['channels']:
                    tmp = {
                        'Из узла': channel['Из узла'],
                        'В узел': channel['В узел'],
                        'Связь': channel['Связь']
                    }
                    self.channels.append(tmp)

            # Обновляем интерфейс
            self.put_info(self.ps, self.loads)
            self.show_graph()

        except Exception as e:
            error(f"Ошибка при чтении файла: {str(e)}")

    def find_min_cost_channel(self, flow):
        """
        Находит подходящий канал с минимальной ценой для заданного потока.
        :param flow: Текущий поток через ребро (в бит/с).
        :return: Название подходящего канала или None, если подходящий канал не найден.
        """
        suitable_channels = []
        for channel in self.chs:
            bandwidth = int(
                channel['Пропускная способность'].split()[0])  # Извлекаем числовое значение пропускной способности
            if bandwidth >= flow:
                cost = int(channel['Стоимость аренды'].split()[0])  # Извлекаем числовое значение стоимости
                suitable_channels.append((channel['Канал'], cost))

        if suitable_channels:
            # Выбираем канал с минимальной ценой
            return min(suitable_channels, key=lambda x: x[1])[0]
        return None  # Если подходящий канал не найден

    def print_channel_selection(self, channel_flows):
        """
        Выводит информацию о выбранных каналах с минимальной ценой для каждого ребра с ненулевым потоком.
        :param channel_flows: Словарь с потоками для каждого ребра.
        """
        for edge, flow in channel_flows.items():
            if flow > 0:  # Только для рёбер с ненулевой нагрузкой
                node1, node2 = edge
                channel_name = self.find_min_cost_channel(flow)
                if channel_name:
                    print(f"{node1} - {node2} - {channel_name}")
                else:
                    print(f"{node1} - {node2} - Подходящий канал не найден")

    def find_min_cost_router(self, flow):
        """
        Находит подходящий маршрутизатор с минимальной ценой для заданного потока.
        :param flow: Суммарный поток через узел (в бит/с).
        :return: Название подходящего маршрутизатора или None, если подходящий маршрутизатор не найден.
        """
        suitable_routers = []
        for router in self.rs:
            bandwidth = int(
                router['Пропускная способность'].split()[0])  # Извлекаем числовое значение пропускной способности
            if bandwidth >= flow:
                cost = int(router['Стоимость'].split()[0])  # Извлекаем числовое значение стоимости
                suitable_routers.append((router['Модель'], cost))

        if suitable_routers:
            # Выбираем маршрутизатор с минимальной ценой
            return min(suitable_routers, key=lambda x: x[1])[0]
        return None  # Если подходящий маршрутизатор не найден

    def print_router_selection(self, node_flows):
        """
        Выводит информацию о выбранных маршрутизаторах с минимальной ценой для каждого узла с ненулевой нагрузкой.
        :param node_flows: Словарь с потоками для каждого узла.
        """
        for node, flow in node_flows.items():
            if flow > 0:  # Только для узлов с ненулевой нагрузкой
                router_name = self.find_min_cost_router(flow)
                if router_name:
                    print(f"{node} - {router_name}")
                else:
                    print(f"{node} - Подходящий маршрутизатор не найден")

    def calculate_edge_delays(self, channel_flows, selected_channels, packet_size):
        """
        Вычисляет задержку для каждого ребра с ненулевой нагрузкой.
        :param channel_flows: Словарь с потоками для каждого ребра.
        :param selected_channels: Словарь с выбранными каналами для каждого ребра.
        :param packet_size: Размер пакета (в битах).
        :return: Словарь с задержками для каждого ребра.
        """
        edge_delays = {}
        for edge, flow in channel_flows.items():
            if flow > 0:  # Только для рёбер с ненулевой нагрузкой
                if edge in selected_channels:
                    channel_name = selected_channels[edge]
                    # Находим пропускную способность выбранного канала
                    for channel in self.chs:
                        if channel['Канал'] == channel_name:
                            bandwidth = int(channel['Пропускная способность'].split()[0])  # Переводим в бит/с
                            break
                    # Проверяем, что поток не превышает пропускную способность
                    if bandwidth > flow:
                        delay = packet_size / (bandwidth - flow)
                        edge_delays[edge] = delay
                    else:
                        edge_delays[edge] = float('inf')  # Задержка бесконечна, если канал перегружен
        return edge_delays

    def calculate_average_delay(self, edge_delays):
        """
        Вычисляет среднюю задержку по сети.
        :param edge_delays: Словарь с задержками для каждого ребра.
        :return: Средняя задержка.
        """
        if not edge_delays:
            return 0  # Если рёбер с ненулевой нагрузкой нет, задержка равна 0

        total_delay = sum(edge_delays.values())
        return total_delay / len(edge_delays)

    def print_packet_delays(self, channel_flows):
        """
        Выводит среднюю задержку для каждого размера пакета.
        :param channel_flows: Словарь с потоками для каждого ребра.
        """
        for pkg in self.pkgs:
            packet_size = int(pkg['Размер пакета'].split()[0])  # Извлекаем размер пакета (в битах)
            edge_delays = self.calculate_edge_delays(channel_flows, packet_size)
            average_delay = self.calculate_average_delay(edge_delays)
            print(f"{pkg['Размер пакета']} - {average_delay:.6f} секунд")

    def find_min_delay_configuration(self, channel_flows, node_flows):
        """
        Выбирает каналы и маршрутизаторы с минимальной задержкой.
        :param channel_flows: Словарь с потоками для каждого ребра.
        :param node_flows: Словарь с потоками для каждого узла.
        :return: Словарь с конфигурацией (каналы, маршрутизаторы, средняя задержка, стоимость).
        """
        config = {
            'channels': {},
            'routers': {},
            'average_delay': 0,
            'total_cost': 0
        }

        # Выбираем каналы с максимальной пропускной способностью
        for edge, flow in channel_flows.items():
            if flow > 0:
                # Выбираем канал с максимальной пропускной способностью
                max_bandwidth = 0
                selected_channel = None
                for channel in self.chs:
                    bandwidth = int(channel['Пропускная способность'].split()[0])  # Переводим в бит/с
                    if bandwidth >= flow and bandwidth > max_bandwidth:
                        max_bandwidth = bandwidth
                        selected_channel = channel
                if selected_channel:
                    config['channels'][edge] = selected_channel['Канал']
                    config['total_cost'] += int(selected_channel['Стоимость аренды'].split()[0])

        # Выбираем маршрутизаторы с максимальной пропускной способностью
        for node, flow in node_flows.items():
            if flow > 0:
                # Выбираем маршрутизатор с максимальной пропускной способностью
                max_bandwidth = 0
                selected_router = None
                for router in self.rs:
                    bandwidth = int(router['Пропускная способность'].split()[0])  # Переводим в бит/с
                    if bandwidth >= flow and bandwidth > max_bandwidth:
                        max_bandwidth = bandwidth
                        selected_router = router
                if selected_router:
                    config['routers'][node] = selected_router['Модель']
                    config['total_cost'] += int(selected_router['Стоимость'].split()[0])

        # Вычисляем среднюю задержку
        packet_size = int(self.pkgs[0]['Размер пакета'].split()[0])  # Используем первый пакет для расчёта задержки
        edge_delays = self.calculate_edge_delays(channel_flows, config['channels'], packet_size)
        config['average_delay'] = self.calculate_average_delay(edge_delays)

        return config

    def find_min_cost_configuration(self, channel_flows, node_flows):
        """
        Выбирает каналы и маршрутизаторы с минимальной стоимостью.
        :param channel_flows: Словарь с потоками для каждого ребра.
        :param node_flows: Словарь с потоками для каждого узла.
        :return: Словарь с конфигурацией (каналы, маршрутизаторы, средняя задержка, стоимость).
        """
        config = {
            'channels': {},
            'routers': {},
            'average_delay': 0,
            'total_cost': 0
        }

        # Выбираем каналы с минимальной стоимостью
        for edge, flow in channel_flows.items():
            if flow > 0:
                # Выбираем канал с минимальной стоимостью
                min_cost = float('inf')
                selected_channel = None
                for channel in self.chs:
                    bandwidth = int(channel['Пропускная способность'].split()[0])  # Переводим в бит/с
                    cost = int(channel['Стоимость аренды'].split()[0])
                    if bandwidth >= flow and cost < min_cost:
                        min_cost = cost
                        selected_channel = channel
                if selected_channel:
                    config['channels'][edge] = selected_channel['Канал']
                    config['total_cost'] += min_cost

        # Выбираем маршрутизаторы с минимальной стоимостью
        for node, flow in node_flows.items():
            if flow > 0:
                # Выбираем маршрутизатор с минимальной стоимостью
                min_cost = float('inf')
                selected_router = None
                for router in self.rs:
                    bandwidth = int(router['Пропускная способность'].split()[0])  # Переводим в бит/с
                    cost = int(router['Стоимость'].split()[0])
                    if bandwidth >= flow and cost < min_cost:
                        min_cost = cost
                        selected_router = router
                if selected_router:
                    config['routers'][node] = selected_router['Модель']
                    config['total_cost'] += min_cost

        # Вычисляем среднюю задержку
        packet_size = int(self.pkgs[0]['Размер пакета'].split()[0])  # Используем первый пакет для расчёта задержки
        edge_delays = self.calculate_edge_delays(channel_flows, config['channels'], packet_size)
        config['average_delay'] = self.calculate_average_delay(edge_delays)

        return config

    def get_best_channels(self, flow, top_n=3):
        """
        Возвращает top_n каналов с наименьшей стоимостью для заданного потока.
        """
        suitable_channels = []
        for channel in self.chs:
            bandwidth = int(channel['Пропускная способность'].split()[0])
            if bandwidth >= flow:
                cost = int(channel['Стоимость аренды'].split()[0])
                suitable_channels.append((channel, cost))

        # Сортируем по стоимости и выбираем top_n
        suitable_channels.sort(key=lambda x: x[1])
        return [x[0] for x in suitable_channels[:top_n]]

    def get_best_routers(self, flow, top_n=3):
        """
        Возвращает top_n маршрутизаторов с наименьшей стоимостью для заданного потока.
        """
        suitable_routers = []
        for router in self.rs:
            bandwidth = int(router['Пропускная способность'].split()[0])
            if bandwidth >= flow:
                cost = int(router['Стоимость'].split()[0])
                suitable_routers.append((router, cost))

        # Сортируем по стоимости и выбираем top_n
        suitable_routers.sort(key=lambda x: x[1])
        return [x[0] for x in suitable_routers[:top_n]]

    def normalize_value(self, value, min_value, max_value):
        """
        Нормализует значение в диапазоне от 0 до 1.
        """
        if max_value == min_value:
            return 0  # Если все значения одинаковы, возвращаем 0
        return (value - min_value) / (max_value - min_value)

    def calculate_total_score(self, cost, delay, min_cost, max_cost, min_delay, max_delay, alpha=0.5):
        """
        Вычисляет общий показатель на основе нормализованных стоимости и задержки.
        """
        normalized_cost = self.normalize_value(cost, min_cost, max_cost)
        normalized_delay = self.normalize_value(delay, min_delay, max_delay)
        return alpha * normalized_delay + (1 - alpha) * normalized_cost

    def evaluate_configuration(self, config, channel_flows, packet_size):
        """
        Оценивает конфигурацию: вычисляет стоимость и среднюю задержку.
        """
        total_cost = 0
        edge_delays = {}

        # Вычисляем стоимость и задержку для каналов
        for edge, channel in config['channels'].items():
            bandwidth = int(channel['Пропускная способность'].split()[0])
            cost = int(channel['Стоимость аренды'].split()[0])
            flow = channel_flows[edge]

            total_cost += cost

            if bandwidth > flow:
                delay = packet_size / (bandwidth - flow)
                edge_delays[edge] = delay
            else:
                edge_delays[edge] = float('inf')  # Канал перегружен

        # Вычисляем стоимость для маршрутизаторов
        for node, router in config['routers'].items():
            cost = int(router['Стоимость'].split()[0])
            total_cost += cost

        # Вычисляем среднюю задержку
        if edge_delays:
            average_delay = sum(edge_delays.values()) / len(edge_delays)
        else:
            average_delay = 0

        return {
            'total_cost': total_cost,
            'average_delay': average_delay,
        }

    def generate_possible_configurations(self, channel_flows, node_flows, top_n=3):
        """
        Генерирует все возможные конфигурации, используя только top_n лучших каналов и маршрутизаторов.
        """
        configurations = []

        # Генерация конфигураций для каналов
        channel_options = {}
        for edge, flow in channel_flows.items():
            if flow > 0:
                channel_options[edge] = self.get_best_channels(flow, top_n)

        # Генерация конфигураций для маршрутизаторов
        router_options = {}
        for node, flow in node_flows.items():
            if flow > 0:
                router_options[node] = self.get_best_routers(flow, top_n)

        # Формируем все возможные комбинации
        from itertools import product

        # Получаем все возможные комбинации каналов
        channel_combinations = list(product(*channel_options.values()))

        # Получаем все возможные комбинации маршрутизаторов
        router_combinations = list(product(*router_options.values()))

        # Формируем полные конфигурации
        for ch_comb in channel_combinations:
            for rt_comb in router_combinations:
                config = {
                    'channels': {edge: ch for edge, ch in zip(channel_options.keys(), ch_comb)},
                    'routers': {node: rt for node, rt in zip(router_options.keys(), rt_comb)},
                }
                configurations.append(config)

        return configurations

    def find_optimal_configuration(self, channel_flows, node_flows, packet_size, alpha=0.5, top_n=3):
        """
        Находит оптимальную конфигурацию, используя только top_n лучших каналов и маршрутизаторов.
        """
        # Генерируем все возможные конфигурации
        configurations = self.generate_possible_configurations(channel_flows, node_flows, top_n)

        # Вычисляем минимальные и максимальные значения стоимости и задержки
        costs = []
        delays = []
        for config in configurations:
            evaluation = self.evaluate_configuration(config, channel_flows, packet_size)
            costs.append(evaluation['total_cost'])
            delays.append(evaluation['average_delay'])

        min_cost = min(costs)
        max_cost = max(costs)
        min_delay = min(delays)
        max_delay = max(delays)

        # Выбираем конфигурацию с минимальным общим показателем
        best_config = None
        best_score = float('inf')

        for config in configurations:
            evaluation = self.evaluate_configuration(config, channel_flows, packet_size)
            score = self.calculate_total_score(
                evaluation['total_cost'], evaluation['average_delay'],
                min_cost, max_cost, min_delay, max_delay, alpha
            )

            if score < best_score:
                best_score = score
                best_config = config

        # Возвращаем лучшую конфигурацию
        if best_config:
            evaluation = self.evaluate_configuration(best_config, channel_flows, packet_size)
            return {
                'channels': best_config['channels'],
                'routers': best_config['routers'],
                'average_delay': evaluation['average_delay'],
                'total_cost': evaluation['total_cost'],
            }
        return None


app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()
