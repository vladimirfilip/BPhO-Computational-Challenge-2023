from typing import Callable

from PyQt6 import QtCore, QtGui, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from pages import OrbitsPage, SpirographPage, OrbitsPageSettings, PageClasses, PageIndexes
import sys
import matplotlib

matplotlib.use('QtAgg')


class FigureCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot()
        super(FigureCanvas, self).__init__(fig)

    def set_figure(self, figure: Figure):
        self.axes = figure.add_subplot()

    def plot(self, *args):
        self.axes.plot(*args)


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

        # sc = MplCanvas(self, width=5, height=4, dpi=100)
        # sc.axes.plot([0, 1, 2, 3, 4], [10, 1, 20, 3, 40])
        # #
        # # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
        # #
        # toolbar = NavigationToolbar(sc, self)
        # layout = QtWidgets.QVBoxLayout()
        # layout.addWidget(toolbar)
        # layout.addWidget(sc)
        # #
        # # Create a placeholder widget to hold our toolbar and canvas.
        # #
        # widget = QtWidgets.QWidget()
        # widget.setLayout(layout)
        tab_widget = QtWidgets.QTabWidget()
        self.central_widget = tab_widget
        # tab_widget.addTab(widget, "Demo")
        self.set_tabs(tab_widget)
        #tab_widget.setTabVisible(2, False)
        self.setCentralWidget(tab_widget)
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
