from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMessageBox

from channel_add import Ui_Dialog


def is_number(n: str):
    """is_number(n) Проверяет, является ли n числом"""
    if len(n) == 0 or (n[0] == '-' and any(x.isdigit() is False for x in n[1:])
                       or (n[0] != '-' and any(x.isdigit() is False for x in n))):
        return False
    return True


def error(message: str):
    """error(message) выводит сообщение message в появляющемся окне"""
    msgBox = QMessageBox()
    msgBox.setWindowTitle("Внимание!")
    # message = message.split(':')[1][1:].capitalize()
    msgBox.setText(message)
    msgBox.exec()


class AddChannel(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self):
        super(AddChannel, self).__init__()
        self.setupUi(self)

        self.x1, self.x2 = "", ""
        self.cost = 0
        self.bandwidth = 0
        self.correct_info = False

        self.addButton.clicked.connect(self.add_chnl)

    def add_chnl(self):
        x1, x2 = self.lineFirst.text(), self.lineSecond.text()
        bandwidth, cost = self.lineBandwidth.text(), self.lineCost.text()
        if len(x1) == 0:
            error("Неверный ввод первой точки")
            return
        self.x1 = x1
        if len(x2) == 0:
            error("Неверный ввод второй точки")
            return
        self.x2 = x2
        if is_number(bandwidth):
            if int(bandwidth) <= 0:
                error("Пропускная способность не может быть меньше нуля!")
                return
            self.bandwidth = int(bandwidth)
        else:
            error("Некорректная пропускная способность!")
            return
        if is_number(cost):
            if int(cost) <= 0:
                error("Стоимость не может быть меньше нуля!")
                return
            self.cost = int(cost)
        else:
            error("Некорректная стоимость!")
            return

        self.correct_info = True
        self.close()

    def clear(self):
        self.x1, self.x2 = "", ""
        self.bandwidth, self.cost = 0, 0
        self.correct_info = False
