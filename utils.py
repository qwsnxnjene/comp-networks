from collections import deque

from PyQt6 import QtWidgets
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QAbstractItemView, QMessageBox


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