# Form implementation generated from reading ui file '.\input.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_DialogAdd(object):
    def setupUi(self, DialogAdd):
        DialogAdd.setObjectName("DialogAdd")
        DialogAdd.resize(542, 761)
        self.labelInput = QtWidgets.QLabel(parent=DialogAdd)
        self.labelInput.setGeometry(QtCore.QRect(20, 10, 121, 41))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labelInput.setFont(font)
        self.labelInput.setObjectName("labelInput")
        self.inputNumOfPoints = QtWidgets.QLineEdit(parent=DialogAdd)
        self.inputNumOfPoints.setGeometry(QtCore.QRect(160, 20, 61, 20))
        self.inputNumOfPoints.setObjectName("inputNumOfPoints")
        self.tablePointInput = QtWidgets.QTableWidget(parent=DialogAdd)
        self.tablePointInput.setEnabled(False)
        self.tablePointInput.setGeometry(QtCore.QRect(10, 90, 431, 151))
        self.tablePointInput.setObjectName("tablePointInput")
        self.tablePointInput.setColumnCount(0)
        self.tablePointInput.setRowCount(0)
        self.labelInput_2 = QtWidgets.QLabel(parent=DialogAdd)
        self.labelInput_2.setEnabled(False)
        self.labelInput_2.setGeometry(QtCore.QRect(10, 60, 161, 41))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labelInput_2.setFont(font)
        self.labelInput_2.setObjectName("labelInput_2")
        self.labelInput_3 = QtWidgets.QLabel(parent=DialogAdd)
        self.labelInput_3.setEnabled(False)
        self.labelInput_3.setGeometry(QtCore.QRect(10, 230, 131, 41))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labelInput_3.setFont(font)
        self.labelInput_3.setObjectName("labelInput_3")
        self.tableLoads = QtWidgets.QTableWidget(parent=DialogAdd)
        self.tableLoads.setEnabled(False)
        self.tableLoads.setGeometry(QtCore.QRect(10, 260, 251, 111))
        self.tableLoads.setObjectName("tableLoads")
        self.tableLoads.setColumnCount(0)
        self.tableLoads.setRowCount(0)
        self.tableRoutersInput = QtWidgets.QTableWidget(parent=DialogAdd)
        self.tableRoutersInput.setEnabled(False)
        self.tableRoutersInput.setGeometry(QtCore.QRect(10, 550, 431, 161))
        self.tableRoutersInput.setObjectName("tableRoutersInput")
        self.tableRoutersInput.setColumnCount(0)
        self.tableRoutersInput.setRowCount(0)
        self.labelInput_4 = QtWidgets.QLabel(parent=DialogAdd)
        self.labelInput_4.setEnabled(False)
        self.labelInput_4.setGeometry(QtCore.QRect(10, 370, 161, 41))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labelInput_4.setFont(font)
        self.labelInput_4.setObjectName("labelInput_4")
        self.tableChannelsInput = QtWidgets.QTableWidget(parent=DialogAdd)
        self.tableChannelsInput.setEnabled(False)
        self.tableChannelsInput.setGeometry(QtCore.QRect(10, 410, 431, 111))
        self.tableChannelsInput.setObjectName("tableChannelsInput")
        self.tableChannelsInput.setColumnCount(0)
        self.tableChannelsInput.setRowCount(0)
        self.labelInput_5 = QtWidgets.QLabel(parent=DialogAdd)
        self.labelInput_5.setEnabled(False)
        self.labelInput_5.setGeometry(QtCore.QRect(10, 520, 201, 41))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labelInput_5.setFont(font)
        self.labelInput_5.setObjectName("labelInput_5")
        self.checkAuto = QtWidgets.QCheckBox(parent=DialogAdd)
        self.checkAuto.setGeometry(QtCore.QRect(20, 50, 251, 17))
        self.checkAuto.setObjectName("checkAuto")
        self.createButton = QtWidgets.QPushButton(parent=DialogAdd)
        self.createButton.setGeometry(QtCore.QRect(230, 19, 75, 23))
        self.createButton.setObjectName("createButton")
        self.tablePackagesInput = QtWidgets.QTableWidget(parent=DialogAdd)
        self.tablePackagesInput.setEnabled(False)
        self.tablePackagesInput.setGeometry(QtCore.QRect(280, 260, 161, 141))
        self.tablePackagesInput.setObjectName("tablePackagesInput")
        self.tablePackagesInput.setColumnCount(0)
        self.tablePackagesInput.setRowCount(0)
        self.labelInput_6 = QtWidgets.QLabel(parent=DialogAdd)
        self.labelInput_6.setEnabled(False)
        self.labelInput_6.setGeometry(QtCore.QRect(280, 230, 131, 41))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labelInput_6.setFont(font)
        self.labelInput_6.setObjectName("labelInput_6")
        self.pushButton = QtWidgets.QPushButton(parent=DialogAdd)
        self.pushButton.setGeometry(QtCore.QRect(150, 720, 231, 31))
        self.pushButton.setObjectName("pushButton")
        self.copyButtonPackages = QtWidgets.QPushButton(parent=DialogAdd)
        self.copyButtonPackages.setGeometry(QtCore.QRect(450, 180, 75, 23))
        self.copyButtonPackages.setObjectName("copyButtonPackages")
        self.deleteButtonPackages = QtWidgets.QPushButton(parent=DialogAdd)
        self.deleteButtonPackages.setGeometry(QtCore.QRect(450, 132, 75, 23))
        self.deleteButtonPackages.setObjectName("deleteButtonPackages")
        self.addButtonPackages = QtWidgets.QPushButton(parent=DialogAdd)
        self.addButtonPackages.setGeometry(QtCore.QRect(450, 90, 75, 23))
        self.addButtonPackages.setObjectName("addButtonPackages")
        self.addButtonChannels = QtWidgets.QPushButton(parent=DialogAdd)
        self.addButtonChannels.setGeometry(QtCore.QRect(450, 410, 75, 23))
        self.addButtonChannels.setObjectName("addButtonChannels")
        self.copyButtonChannels = QtWidgets.QPushButton(parent=DialogAdd)
        self.copyButtonChannels.setGeometry(QtCore.QRect(450, 500, 75, 23))
        self.copyButtonChannels.setObjectName("copyButtonChannels")
        self.deleteButtonChannels = QtWidgets.QPushButton(parent=DialogAdd)
        self.deleteButtonChannels.setGeometry(QtCore.QRect(450, 452, 75, 23))
        self.deleteButtonChannels.setObjectName("deleteButtonChannels")
        self.deleteButtonRouters = QtWidgets.QPushButton(parent=DialogAdd)
        self.deleteButtonRouters.setGeometry(QtCore.QRect(450, 591, 75, 23))
        self.deleteButtonRouters.setObjectName("deleteButtonRouters")
        self.copyButtonRouters = QtWidgets.QPushButton(parent=DialogAdd)
        self.copyButtonRouters.setGeometry(QtCore.QRect(450, 639, 75, 23))
        self.copyButtonRouters.setObjectName("copyButtonRouters")
        self.addButtonRouters = QtWidgets.QPushButton(parent=DialogAdd)
        self.addButtonRouters.setGeometry(QtCore.QRect(450, 549, 75, 23))
        self.addButtonRouters.setObjectName("addButtonRouters")
        self.labelInput.raise_()
        self.inputNumOfPoints.raise_()
        self.labelInput_2.raise_()
        self.labelInput_3.raise_()
        self.labelInput_4.raise_()
        self.labelInput_5.raise_()
        self.checkAuto.raise_()
        self.createButton.raise_()
        self.labelInput_6.raise_()
        self.pushButton.raise_()
        self.tablePackagesInput.raise_()
        self.tableChannelsInput.raise_()
        self.tableLoads.raise_()
        self.tableRoutersInput.raise_()
        self.tablePointInput.raise_()
        self.copyButtonPackages.raise_()
        self.deleteButtonPackages.raise_()
        self.addButtonPackages.raise_()
        self.addButtonChannels.raise_()
        self.copyButtonChannels.raise_()
        self.deleteButtonChannels.raise_()
        self.deleteButtonRouters.raise_()
        self.copyButtonRouters.raise_()
        self.addButtonRouters.raise_()

        self.retranslateUi(DialogAdd)
        QtCore.QMetaObject.connectSlotsByName(DialogAdd)

    def retranslateUi(self, DialogAdd):
        _translate = QtCore.QCoreApplication.translate
        DialogAdd.setWindowTitle(_translate("DialogAdd", "Ввод данных"))
        self.labelInput.setText(_translate("DialogAdd", "Количество узлов:"))
        self.labelInput_2.setText(_translate("DialogAdd", "Информация об узлах"))
        self.labelInput_3.setText(_translate("DialogAdd", "Матрица нагрузки"))
        self.labelInput_4.setText(_translate("DialogAdd", "Информация о каналах"))
        self.labelInput_5.setText(_translate("DialogAdd", "Доступные маршрутизаторы"))
        self.checkAuto.setText(_translate("DialogAdd", "Автоматическое создание графа"))
        self.createButton.setText(_translate("DialogAdd", "Создать"))
        self.labelInput_6.setText(_translate("DialogAdd", "Список пакетов:"))
        self.pushButton.setText(_translate("DialogAdd", "Готово"))
        self.copyButtonPackages.setText(_translate("DialogAdd", "Копировать"))
        self.deleteButtonPackages.setText(_translate("DialogAdd", "Удалить"))
        self.addButtonPackages.setText(_translate("DialogAdd", "Добавить"))
        self.addButtonChannels.setText(_translate("DialogAdd", "Добавить"))
        self.copyButtonChannels.setText(_translate("DialogAdd", "Копировать"))
        self.deleteButtonChannels.setText(_translate("DialogAdd", "Удалить"))
        self.deleteButtonRouters.setText(_translate("DialogAdd", "Удалить"))
        self.copyButtonRouters.setText(_translate("DialogAdd", "Копировать"))
        self.addButtonRouters.setText(_translate("DialogAdd", "Добавить"))
