from typing import Callable

from PyQt6 import QtWidgets
from pages import OrbitsPage, SpirographPage, OrbitsPageSettings, PageClasses, PageIndexes
import sys


class MainWindow(QtWidgets.QMainWindow):
    __TAB_DATA = [
        (OrbitsPage, "Orbits", "Detailed orbit simulator in 2D and 3D", True),
        (OrbitsPageSettings, "", "", False),
        (SpirographPage, "Spirograph", "Spirograph generator", True)
    ]

    def __init__(self, *args, **kwargs):
        for i in range(len(MainWindow.__TAB_DATA)):
            expected_class = PageClasses[PageIndexes(i).name].value
            assert expected_class == MainWindow.__TAB_DATA[i][0]
        super(MainWindow, self).__init__(*args, **kwargs)
        tab_widget = QtWidgets.QTabWidget()
        self.central_widget = tab_widget
        self.set_tabs(tab_widget)
        self.setCentralWidget(tab_widget)
        self.setStyleSheet(''' font-size: 14px; ''')
        self.show()

    def set_tabs(self, tab_widget: QtWidgets.QTabWidget):
        for i, t in enumerate(MainWindow.__TAB_DATA):
            contents_class, tab_name, tooltip, is_visible = t
            tab_widget.addTab(contents_class(self), tab_name)
            tab_widget.setTabToolTip(i, tooltip)
            tab_widget.setTabVisible(i, is_visible)

    def switch_to(self, widget_index: int, post_func: Callable = None):
        self.central_widget.setCurrentIndex(widget_index)
        if post_func:
            post_func(self.central_widget.currentWidget())


app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec()
