from PyQt6 import QtCore, QtGui, QtWidgets


class ValueViewer(QtWidgets.QVBoxLayout):
    def __init__(self, lbl_txt: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.addWidget(QtWidgets.QLabel(lbl_txt))
        self.label = QtWidgets.QLabel("-")
        self.addWidget(self.label)

    def set_text(self, new_text: str):
        self.label.setText(new_text if new_text else "-")
