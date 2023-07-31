from PyQt6 import QtCore, QtGui, QtWidgets


class Page1(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QGridLayout()

        layout.setGeometry(QtCore.QRect(QtCore.QPoint(0, 0), QtCore.QPoint(1100, 700)))
        label = QtWidgets.QLabel(self)
        pixmap = QtGui.QPixmap('task1.png')
        label.setPixmap(pixmap)
        label.setScaledContents(True)
        label.setGeometry(0, 0, 1100, 700)
        layout.addWidget(label, 0, 0)
        self.setLayout(QtWidgets.QVBoxLayout())


class Page2(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()


class Page3(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()


class Page4(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()


class Page5(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()


class Page6(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()


class Page7(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()