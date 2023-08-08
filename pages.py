from PyQt6 import QtCore, QtGui, QtWidgets
from enum import Enum

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

PLANETS: list[str] = ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]


class PageIndexes(Enum):
    ORBITS_PAGE = 0
    ORBITS_PAGE_SETTINGS = 1
    SPIROGRAPH_PAGE = 2


class OrbitSimulationSettings:
    SETTINGS: dict = {
        "Centre of orbit": "Sun",
        "Objects to show": ["Sun"] + PLANETS,
        "Animation Speed": 1,
        "Orbit time": 1,
        "View type": "2D"
    }


class FigureCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot()
        super(FigureCanvas, self).__init__(fig)

    def set_figure(self, figure: Figure):
        self.axes = figure.add_subplot()

    def plot(self, *args):
        self.axes.plot(*args)


class OrbitsPage(QtWidgets.QWidget):
    ORBITS_STATS: dict[str, QtWidgets.QLabel] = {
        "Coordinates": None,
        "Mass": None,
        "Angular velocity": None,
        "Linear velocity": None,
        "Distance from centre": None,
        "Orbital angle": None,
        "Eccentricity": None,
        "Semi-major axis": None,
        "Semi-minor axis": None,
        "Orbital period": None,
    }

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setParent(parent)
        root_layout = QtWidgets.QHBoxLayout()
        self.sim_settings = OrbitSimulationSettings()
        self.figure_canvas = FigureCanvas(self)
        self.figure_canvas.plot([0, 1, 2, 3, 4], [10, 1, 20, 3, 40])
        graph_layout = QtWidgets.QVBoxLayout()
        toolbar = NavigationToolbar(self.figure_canvas, self)
        graph_layout.addWidget(toolbar)
        graph_layout.addWidget(self.figure_canvas)
        settings_button = QtWidgets.QPushButton("Settings")
        settings_button.clicked.connect(self.on_settings_button_click)
        graph_layout.addWidget(settings_button)
        root_layout.addLayout(graph_layout)
        #
        # Creating layout and widgets for user to pick planet to see orbit stats on
        #
        planet_picker_layout = QtWidgets.QHBoxLayout()
        planet_picker_layout.addWidget(QtWidgets.QLabel("Planet: "))
        planet_picker_dropdown = QtWidgets.QComboBox()
        planet_picker_dropdown.addItems(PLANETS)
        planet_picker_dropdown.currentIndexChanged.connect(self.on_planet_dropdown_changed)
        planet_picker_layout.addWidget(planet_picker_dropdown)
        #
        # Creating layout and widgets to display planet orbit stats
        #
        for stat_name in OrbitsPage.ORBITS_STATS:
            OrbitsPage.ORBITS_STATS[stat_name] = QtWidgets.QLabel("N/A")
        stats_layout = QtWidgets.QGridLayout()
        for i, orbit_stat in enumerate(OrbitsPage.ORBITS_STATS.keys()):
            stat_name, stat_value = orbit_stat, OrbitsPage.ORBITS_STATS[orbit_stat]
            stats_layout.addWidget(QtWidgets.QLabel(stat_name), i // 2 * 2, i % 2, 1, 1)
            stats_layout.addWidget(stat_value, i // 2 * 2 + 1, i % 2, 1, 1)
        controls_layout = QtWidgets.QVBoxLayout()
        controls_layout.addLayout(planet_picker_layout)
        controls_layout.addLayout(stats_layout)
        root_layout.addLayout(controls_layout)
        self.setLayout(root_layout)

    @QtCore.pyqtSlot(int)
    def on_planet_dropdown_changed(self, new_index: int):
        new_planet: str = PLANETS[new_index]
        # TODO: add binding to engine to set new stats on the new planet
        pass

    def on_settings_button_click(self):
        self.parent.switch_to(PageIndexes.ORBITS_PAGE_SETTINGS.value)

    def update_graph(self):
        print("FROM UPDATE_GRAPH")
        print(self.sim_settings.SETTINGS)
        # Called when simulation settings have been updated
        # TODO: create new figure with new simulation settings
        pass

    @staticmethod
    def set_stats(new_stats: dict[str, str]):
        assert len(new_stats) == len(OrbitsPage.ORBITS_STATS)
        for k, v in new_stats.items():
            OrbitsPage.ORBITS_STATS[k].setText(new_stats[k])


class OrbitsPageSettings(QtWidgets.QWidget):
    CENTRE_OF_ORBIT_OPTIONS = ["Sun"] + PLANETS
    OBJECTS_TO_SHOW_OPTIONS = ["Sun"] + PLANETS
    def __init__(self, parent):
        super().__init__()
        self.centre_of_orbit_picker = None
        self.orbit_time_slider = None
        self.orbit_time_indicator = None
        self._3d_view_type_btn = None
        self._2d_view_type_btn = None
        self.anim_speed_indicator = None
        self.anim_speed_slider = None
        self.objects_to_show_checkboxes: list[QtWidgets.QCheckBox] = []
        self.parent = parent
        self.settings = OrbitSimulationSettings()
        self.original_settings: dict = self.settings.SETTINGS.copy()
        root_layout = QtWidgets.QVBoxLayout()
        button_layout = QtWidgets.QHBoxLayout()
        reset_button = QtWidgets.QPushButton("Reset")
        reset_button.clicked.connect(self.on_reset_button_pressed)
        back_button = QtWidgets.QPushButton("Back")
        back_button.clicked.connect(self.on_back_button_pressed)
        button_layout.addWidget(reset_button)
        button_layout.addWidget(back_button)
        root_layout.addLayout(button_layout)
        self.controls_layout = QtWidgets.QVBoxLayout()
        self.init_settings_widgets()
        self.set_settings_widget_states()
        root_layout.addLayout(self.controls_layout)
        self.setLayout(root_layout)

    def on_reset_button_pressed(self):
        self.settings.SETTINGS = self.original_settings
        self.set_settings_widget_states()

    def on_back_button_pressed(self):
        self.parent.switch_to(PageIndexes.ORBITS_PAGE.value, post_func=lambda w: w.update_graph())

    def init_settings_widgets(self):
        top_half = QtWidgets.QHBoxLayout()
        centre_of_orbit_layout = QtWidgets.QVBoxLayout()
        centre_of_orbit_layout.addWidget(QtWidgets.QLabel("Center of orbit"))
        self.centre_of_orbit_picker = QtWidgets.QComboBox()
        self.centre_of_orbit_picker.addItems(OrbitsPageSettings.CENTRE_OF_ORBIT_OPTIONS)
        self.centre_of_orbit_picker.currentIndexChanged.connect(self.on_centre_of_orbit_changed)
        centre_of_orbit_layout.addWidget(self.centre_of_orbit_picker)
        top_half.addLayout(centre_of_orbit_layout)
        objects_to_show_layout = QtWidgets.QVBoxLayout()
        objects_to_show_layout.addWidget(QtWidgets.QLabel("Objects to show"))
        self.objects_to_show_checkboxes = []
        for i in range(len(OrbitsPageSettings.OBJECTS_TO_SHOW_OPTIONS)):
            check_box = QtWidgets.QCheckBox(OrbitsPageSettings.OBJECTS_TO_SHOW_OPTIONS[i], self)
            check_box.toggled.connect(lambda: self.on_object_to_show_state_changed(i))
            objects_to_show_layout.addWidget(check_box)
            self.objects_to_show_checkboxes.append(check_box)
        top_half.addLayout(objects_to_show_layout)
        anim_speed_slider_layout = QtWidgets.QVBoxLayout()
        anim_speed_slider_layout.addWidget(QtWidgets.QLabel("Animation Speed"))
        self.anim_speed_slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        original_speed_value = 1
        self.anim_speed_slider.setMinimum(0)
        self.anim_speed_slider.setMaximum(10)
        self.anim_speed_slider.setValue(original_speed_value)
        self.anim_speed_slider.setTickPosition(QtWidgets.QSlider.TickPosition.TicksBelow)
        self.anim_speed_slider.setTickInterval(1)
        self.anim_speed_slider.valueChanged.connect(self.update_anim_speed)
        anim_speed_slider_layout.addWidget(self.anim_speed_slider)
        self.anim_speed_indicator: QtWidgets.QLabel = QtWidgets.QLabel(f"{original_speed_value}x")
        anim_speed_slider_layout.addWidget(self.anim_speed_indicator)
        top_half.addLayout(anim_speed_slider_layout)
        self.controls_layout.addLayout(top_half)
        bottom_half = QtWidgets.QHBoxLayout()
        view_type_layout = QtWidgets.QVBoxLayout()
        view_type_layout.addWidget(QtWidgets.QLabel("View type"))
        view_type_btn_layout = QtWidgets.QHBoxLayout()
        self._2d_view_type_btn = QtWidgets.QRadioButton("2D")
        self._3d_view_type_btn = QtWidgets.QRadioButton("3D")
        self._2d_view_type_btn.toggled.connect(self._2d_view_type_toggled)
        self._3d_view_type_btn.toggled.connect(self._3d_view_type_toggled)
        view_type_btn_layout.addWidget(self._2d_view_type_btn)
        view_type_btn_layout.addWidget(self._3d_view_type_btn)
        view_type_layout.addLayout(view_type_btn_layout)
        bottom_half.addLayout(view_type_layout)
        orbit_time_layout = QtWidgets.QVBoxLayout()
        orbit_time_layout.addWidget(QtWidgets.QLabel("Orbit time (for shortest orbit"))
        self.orbit_time_slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        original_orbit_time_value = 1
        self.orbit_time_slider.setMinimum(1)
        self.orbit_time_slider.setMaximum(10)
        self.orbit_time_slider.setValue(original_orbit_time_value)
        self.orbit_time_slider.setTickPosition(QtWidgets.QSlider.TickPosition.TicksBelow)
        self.orbit_time_slider.setTickInterval(1)
        self.orbit_time_slider.valueChanged.connect(self.update_orbit_time)
        orbit_time_layout.addWidget(self.orbit_time_slider)
        self.orbit_time_indicator = QtWidgets.QLabel(f"{original_orbit_time_value} s")
        orbit_time_layout.addWidget(self.orbit_time_indicator)
        bottom_half.addLayout(orbit_time_layout)
        self.controls_layout.addLayout(bottom_half)

    def set_settings_widget_states(self):
        centre_of_orbit_index = OrbitsPageSettings.CENTRE_OF_ORBIT_OPTIONS.index(self.settings.SETTINGS["Centre of orbit"])
        print(centre_of_orbit_index)
        self.centre_of_orbit_picker.setCurrentIndex(centre_of_orbit_index)
        for i in range(len(self.objects_to_show_checkboxes)):
            checkbox = self.objects_to_show_checkboxes[i]
            print(checkbox.text(), checkbox.text() in self.settings.SETTINGS["Objects to show"])
            checkbox.setChecked(checkbox.text() in self.settings.SETTINGS["Objects to show"])

    def on_centre_of_orbit_changed(self, new_index: int):
        self.settings.SETTINGS["Centre of orbit"] = OrbitsPageSettings.CENTRE_OF_ORBIT_OPTIONS[new_index]

    def on_object_to_show_state_changed(self, index: int):
        print("EVENT CALLED")
        entry = OrbitsPageSettings.OBJECTS_TO_SHOW_OPTIONS[index]
        is_checked = self.objects_to_show_checkboxes[index].isChecked()
        if not is_checked:
            if entry in self.settings.SETTINGS["Objects to show"]:
                self.settings.SETTINGS["Objects to show"].remove(entry)
        else:
            if entry not in self.settings.SETTINGS["Objects to show"]:
                self.settings.SETTINGS["Objects to show"].append(entry)
        self.settings.SETTINGS["Objects to show"] = list(set(self.settings.SETTINGS["Objects to show"]))

    def update_anim_speed(self, new_value: int):
        self.settings.SETTINGS["Animation Speed"] = new_value
        self.anim_speed_indicator.setText(f"{new_value}x")

    def update_orbit_time(self, new_value: int):
        self.settings.SETTINGS["Orbit time"] = new_value
        self.orbit_time_indicator.setText(f"{new_value}s")

    def _2d_view_type_toggled(self):
        self._3d_view_type_btn.setChecked(False)
        self.settings.SETTINGS["View type"] = "2D"

    def _3d_view_type_toggled(self):
        self._2d_view_type_btn.setChecked(False)
        self.settings.SETTINGS["View type"] = "3D"


class SpirographPage(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        layout = QtWidgets.QVBoxLayout()

        layout.addWidget(QtWidgets.QLabel("SPIROGRAPH"))
        self.setLayout(layout)


class PageClasses(Enum):
    ORBITS_PAGE = OrbitsPage
    ORBITS_PAGE_SETTINGS = OrbitsPageSettings
    SPIROGRAPH_PAGE = SpirographPage
