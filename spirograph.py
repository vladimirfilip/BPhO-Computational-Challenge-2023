from PyQt6 import QtCore, QtGui, QtWidgets

PLANETS: list[str] = ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]


class PlanetPicker(QtWidgets.QVBoxLayout):
    def __init__(self, lbl_str: str, start_str: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.addWidget(QtWidgets.QLabel(lbl_str))
        self.picker = QtWidgets.QComboBox()
        self.picker.addItems(PLANETS)
        self.picker.setCurrentIndex(PLANETS.index(start_str))
        self.addWidget(self.picker)


class FloatPicker(QtWidgets.QVBoxLayout):
    def __init__(self, lbl_text: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.addWidget(QtWidgets.QLabel(lbl_text))
        self.line_edit = QtWidgets.QLineEdit()
        self.line_edit.setValidator(QtGui.QDoubleValidator())
        self.addWidget(self.line_edit)


class IntPicker(QtWidgets.QVBoxLayout):
    def __init__(self, lbl_text: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.addWidget(QtWidgets.QLabel(lbl_text))
        self.line_edit = QtWidgets.QLineEdit()
        self.line_edit.setValidator(QtGui.QIntValidator())
        self.addWidget(self.line_edit)

