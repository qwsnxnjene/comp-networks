# Form implementation generated from reading ui file 'input.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_DialogAdd(object):
    def setupUi(self, DialogAdd):
        DialogAdd.setObjectName("DialogAdd")
        DialogAdd.resize(542, 560)
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
        self.tableLoads.setGeometry(QtCore.QRect(10, 260, 431, 231))
        self.tableLoads.setObjectName("tableLoads")
        self.tableLoads.setColumnCount(0)
        self.tableLoads.setRowCount(0)
        self.checkAuto = QtWidgets.QCheckBox(parent=DialogAdd)
        self.checkAuto.setGeometry(QtCore.QRect(20, 50, 251, 17))
        self.checkAuto.setObjectName("checkAuto")
        self.createButton = QtWidgets.QPushButton(parent=DialogAdd)
        self.createButton.setGeometry(QtCore.QRect(230, 19, 75, 23))
        self.createButton.setObjectName("createButton")
        self.copyButtonPackages = QtWidgets.QPushButton(parent=DialogAdd)
        self.copyButtonPackages.setGeometry(QtCore.QRect(450, 180, 75, 23))
        self.copyButtonPackages.setObjectName("copyButtonPackages")
        self.deleteButtonPackages = QtWidgets.QPushButton(parent=DialogAdd)
        self.deleteButtonPackages.setGeometry(QtCore.QRect(450, 132, 75, 23))
        self.deleteButtonPackages.setObjectName("deleteButtonPackages")
        self.addButtonPackages = QtWidgets.QPushButton(parent=DialogAdd)
        self.addButtonPackages.setGeometry(QtCore.QRect(450, 90, 75, 23))
        self.addButtonPackages.setObjectName("addButtonPackages")
        self.pushButton = QtWidgets.QPushButton(parent=DialogAdd)
        self.pushButton.setGeometry(QtCore.QRect(200, 500, 171, 51))
        self.pushButton.setObjectName("pushButton")
        self.labelInput.raise_()
        self.inputNumOfPoints.raise_()
        self.labelInput_2.raise_()
        self.labelInput_3.raise_()
        self.checkAuto.raise_()
        self.createButton.raise_()
        self.tableLoads.raise_()
        self.tablePointInput.raise_()
        self.copyButtonPackages.raise_()
        self.deleteButtonPackages.raise_()
        self.addButtonPackages.raise_()
        self.pushButton.raise_()

        self.retranslateUi(DialogAdd)
        QtCore.QMetaObject.connectSlotsByName(DialogAdd)

    def retranslateUi(self, DialogAdd):
        _translate = QtCore.QCoreApplication.translate
        DialogAdd.setWindowTitle(_translate("DialogAdd", "Ввод данных"))
        self.labelInput.setText(_translate("DialogAdd", "Количество узлов:"))
        self.labelInput_2.setText(_translate("DialogAdd", "Информация об узлах"))
        self.labelInput_3.setText(_translate("DialogAdd", "Матрица нагрузки"))
        self.checkAuto.setText(_translate("DialogAdd", "Автоматическое создание графа"))
        self.createButton.setText(_translate("DialogAdd", "Создать"))
        self.copyButtonPackages.setText(_translate("DialogAdd", "Копировать"))
        self.deleteButtonPackages.setText(_translate("DialogAdd", "Удалить"))
        self.addButtonPackages.setText(_translate("DialogAdd", "Добавить"))
        self.pushButton.setText(_translate("DialogAdd", "Готово"))
