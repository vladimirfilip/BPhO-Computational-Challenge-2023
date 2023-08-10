from typing import Optional

from PyQt6 import QtCore, QtGui, QtWidgets
from enum import Enum

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from orbitsettings import OrbitSimSettings, ObjToShowCheckbox, CentreOfOrbitPicker, AnimSpeedPicker, ViewTypePicker, \
    OrbitTimePicker, SettingsKeys, ViewType
from spirograph import PlanetPicker, FloatPicker, IntPicker
from core_components import ValueViewer

PLANETS: list[str] = ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]


class PageIndexes(Enum):
    ORBITS_PAGE = 0
    ORBITS_PAGE_SETTINGS = 1
    SPIROGRAPH_PAGE = 2


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
    ORBITS_STATS: dict[str, Optional[str]] = {
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
        self.sim_settings = OrbitSimSettings()
        self.figure_canvas = FigureCanvas(self)
        self.figure_canvas.plot([0, 1, 2, 3, 4], [10, 1, 20, 3, 40])
        graph_layout = QtWidgets.QVBoxLayout()
        toolbar = NavigationToolbar(self.figure_canvas, self)
        graph_layout.addWidget(toolbar)
        graph_layout.addWidget(self.figure_canvas)
        settings_btn_layout = QtWidgets.QHBoxLayout()
        settings_btn_layout.addStretch()
        settings_button = QtWidgets.QPushButton("Settings")
        settings_button.clicked.connect(self.on_settings_button_click)
        settings_btn_layout.addWidget(settings_button)
        settings_btn_layout.addStretch()
        graph_layout.addLayout(settings_btn_layout)
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
        stats_layout = QtWidgets.QGridLayout()
        self.stats_components: list[ValueViewer] = []
        for i, orbit_stat in enumerate(OrbitsPage.ORBITS_STATS.keys()):
            stat_name, stat_value = orbit_stat, OrbitsPage.ORBITS_STATS[orbit_stat]
            stats_component = ValueViewer(stat_name)
            stats_component.set_text(stat_value)
            self.stats_components.append(stats_component)
            stats_layout.addLayout(stats_component, i // 2, i % 2, 1, 1)
        controls_layout = QtWidgets.QVBoxLayout()
        controls_layout.addLayout(planet_picker_layout)
        controls_layout.addLayout(stats_layout)
        root_layout.addLayout(controls_layout)
        self.setLayout(root_layout)

    def on_planet_dropdown_changed(self, new_index: int):
        new_planet: str = PLANETS[new_index]
        # TODO: add binding to engine to set new stats on the new planet
        pass

    def on_settings_button_click(self):
        self.parent.switch_to(PageIndexes.ORBITS_PAGE_SETTINGS.value)

    def update_graph(self):
        print("NEW SETTINGS")
        print(self.sim_settings.SETTINGS)
        # Called when simulation settings have been updated
        # TODO: create new figure with new simulation settings
        pass

    def set_stats(self, new_stats: dict[str, str]):
        assert len(new_stats) == len(OrbitsPage.ORBITS_STATS)
        for i, k in enumerate(new_stats.keys()):
            OrbitsPage.ORBITS_STATS[k] = new_stats[k]
            self.stats_components[i].set_text(new_stats[k])


class OrbitsPageSettings(QtWidgets.QWidget):
    OBJECTS_TO_SHOW_OPTIONS = ["Sun"] + PLANETS

    def __init__(self, parent):
        super().__init__()
        self.child_widgets = []
        self.parent = parent
        self.settings = OrbitSimSettings()
        self.original_settings: dict = {
            SettingsKeys.CENTRE_OF_ORBIT.value: "Sun",
            SettingsKeys.OBJECTS_TO_SHOW.value: ["Sun"] + PLANETS,
            SettingsKeys.ANIM_SPEED.value: 1,
            SettingsKeys.ORBIT_TIME.value: 1,
            SettingsKeys.VIEW_TYPE.value: ViewType.TWO_D.value
        }
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
        root_layout.addLayout(self.controls_layout)
        self.setLayout(root_layout)

    def on_reset_button_pressed(self):
        if self.settings.SETTINGS != self.original_settings:
            for k in self.original_settings.keys():
                self.settings.SETTINGS[k] = self.original_settings[k]
            for widget in self.child_widgets:
                widget.set_state()

    def on_back_button_pressed(self):
        self.parent.switch_to(PageIndexes.ORBITS_PAGE.value, post_func=lambda w: w.update_graph())

    def init_settings_widgets(self):
        top_half = QtWidgets.QHBoxLayout()
        top_half.addStretch()
        centre_of_orbit_picker = CentreOfOrbitPicker(self.settings)
        centre_of_orbit_picker.setContentsMargins(5, 5, 5, 5)
        self.child_widgets.append(centre_of_orbit_picker)
        top_half.addLayout(centre_of_orbit_picker)
        objects_to_show_layout = QtWidgets.QVBoxLayout()
        objects_to_show_layout.addWidget(QtWidgets.QLabel("Objects to show"))
        for i in range(len(OrbitsPageSettings.OBJECTS_TO_SHOW_OPTIONS)):
            check_box = ObjToShowCheckbox(self.settings, OrbitsPageSettings.OBJECTS_TO_SHOW_OPTIONS[i], self)
            objects_to_show_layout.addWidget(check_box)
            self.child_widgets.append(check_box)
        objects_to_show_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        objects_to_show_layout.setContentsMargins(10, 5, 10, 5)
        top_half.addLayout(objects_to_show_layout)
        anim_speed_picker = AnimSpeedPicker(self.settings)
        self.child_widgets.append(anim_speed_picker)
        top_half.addLayout(anim_speed_picker)
        top_half.addStretch()
        self.controls_layout.addLayout(top_half)
        bottom_half = QtWidgets.QHBoxLayout()
        view_type_picker = ViewTypePicker(self.settings)
        self.child_widgets.append(view_type_picker)
        bottom_half.addLayout(view_type_picker)
        orbit_time_picker = OrbitTimePicker(self.settings)
        self.child_widgets.append(orbit_time_picker)
        bottom_half.addLayout(orbit_time_picker)
        self.controls_layout.addLayout(bottom_half)


class SpirographPage(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setParent(parent)
        root_layout = QtWidgets.QHBoxLayout()
        self.sim_settings = OrbitSimSettings()
        self.figure_canvas = FigureCanvas(self)
        self.figure_canvas.plot([0, 1, 2, 3, 4], [10, 1, 20, 3, 40])
        graph_layout = QtWidgets.QVBoxLayout()
        toolbar = NavigationToolbar(self.figure_canvas, self)
        graph_layout.addWidget(toolbar)
        graph_layout.addWidget(self.figure_canvas)
        root_layout.addLayout(graph_layout)
        controls_layout = QtWidgets.QVBoxLayout()
        grid_layout = QtWidgets.QGridLayout()
        self.planet1picker: PlanetPicker = PlanetPicker("Planet 1", "Venus")
        self.planet2picker: PlanetPicker = PlanetPicker("Planet 2", "Earth")
        self.time_diff_picker: FloatPicker = FloatPicker("Difference in time")
        self.n_orbits: IntPicker = IntPicker("Number of orbits of outermost planet")

        grid_layout.addLayout(self.planet1picker, 0, 0, 1, 1)
        grid_layout.addLayout(self.planet2picker, 0, 1, 1, 1)
        grid_layout.addLayout(self.time_diff_picker, 1, 0, 1, 1)
        grid_layout.addLayout(self.n_orbits, 1, 1, 1, 1)
        controls_layout.addLayout(grid_layout)
        eval_button = QtWidgets.QPushButton("Evaluate")
        eval_button.pressed.connect(self.on_eval_button_press)
        controls_layout.addWidget(eval_button)
        self.completed_orbits = ValueViewer("Completed orbits")
        self.elapsed_time = ValueViewer("Elapsed time")
        controls_layout.addLayout(self.completed_orbits)
        controls_layout.addLayout(self.elapsed_time)
        root_layout.addLayout(controls_layout)
        self.setLayout(root_layout)

    def on_eval_button_press(self):
        print(self.planet1picker.picker.currentText(),
              self.planet2picker.picker.currentText(),
              self.time_diff_picker.line_edit.text(),
              self.n_orbits.line_edit.text())
        # TODO: integrate functionality to plot spirograph based on input parameters


class PageClasses(Enum):
    ORBITS_PAGE = OrbitsPage
    ORBITS_PAGE_SETTINGS = OrbitsPageSettings
    SPIROGRAPH_PAGE = SpirographPage
