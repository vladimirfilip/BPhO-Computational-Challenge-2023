import sys
import matplotlib

matplotlib.use('QtAgg')

from PyQt6 import QtCore, QtGui, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from pages import Page1, Page2, Page3, Page4, Page5, Page6, Page7


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, pages: list, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        sc = MplCanvas(self, width=5, height=4, dpi=100)
        sc.axes.plot([0, 1, 2, 3, 4], [10, 1, 20, 3, 40])

        # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
        toolbar = NavigationToolbar(sc, self)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(sc)

        # Create a placeholder widget to hold our toolbar and canvas.
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        tab_widget = QtWidgets.QTabWidget()
        tab_widget.addTab(widget, "Demo")
        for i in range(len(pages)):
            tab_widget.addTab(pages[i], f"Task {i + 1}")
        self.setCentralWidget(tab_widget)
        self.show()


app = QtWidgets.QApplication(sys.argv)
w = MainWindow([Page1(), Page2(), Page3(), Page4(), Page5(), Page6(), Page7()])
app.exec()
