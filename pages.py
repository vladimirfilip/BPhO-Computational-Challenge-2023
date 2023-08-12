from typing import Optional
from PyQt6 import QtCore, QtGui, QtWidgets
from enum import Enum

from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
import matplotlib.pyplot as plt

from _3d_animation import Animation3D
from spiro_animation import SpiroAnimation

matplotlib.use('TkAgg')


from _2d_animation import Animation2D
from components import OrbitSimSettings, ViewTypePicker, \
    OrbitTimePicker, SettingsKeys, ViewType, SettingsBtnLayout, \
    HorizontalValuePicker, ValueViewer, VerticalValuePicker

PLANETS: list[str] = ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]


class PageIndexes(Enum):
    ORBITS_PAGE = 0
    ORBITS_PAGE_SETTINGS = 1
    SPIROGRAPH_PAGE = 2


# class FigureCanvas(FigureCanvasQTAgg):
#
#     def __init__(self, parent=None, width=5, height=4, dpi=100):
#         self.fig = Figure(figsize=(10, 10))
#         self.axes = fig.add_subplot()
#         super(FigureCanvas, self).__init__(fig)
#         self.ani = Animation2D("SOLAR_SYSTEM", ["MERCURY", "VENUS", "EARTH"], "SUN", 2.0, 1)
#         self.ani = self.ani.create_animation(fig)
#         self.draw()
#
#     def set_figure(self, figure: Figure):
#         self.axes = figure.add_subplot()
#
#     def plot(self, *args):
#         self.axes.plot(*args)


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
        #
        # Creating the graph canvas and the toolbar to manipulate it
        #
        self.fig = Figure(figsize=(12, 12), dpi=100)
        self.canvas = FigureCanvas(self.fig)
        graph_layout = QtWidgets.QVBoxLayout()
        toolbar = NavigationToolbar(self.canvas, self)
        graph_layout.addWidget(toolbar)
        graph_layout.addWidget(self.canvas)
        settings_btn_layout = SettingsBtnLayout(on_click=self.on_settings_button_click,
                                                btn_width=30,
                                                btn_height=30)
        graph_layout.addLayout(settings_btn_layout)
        root_layout.addLayout(graph_layout)
        self.anim = Animation2D(self.fig, "PROXIMA_CENTAURI", ["d", "b"], "PROXIMA_CENTAURI", 3, 7)
        #
        # Creating layout and widgets for user to pick planet to see orbit stats on
        #
        planet_picker_layout = HorizontalValuePicker(
            lbl_text="Planet: ",
            value_type="from_multiple",
            default_val="Earth",
            choices=PLANETS,
            tooltip="Choose the name of the planet to see orbit stats on",
            on_change=self.on_planet_dropdown_changed,
            fixed_lbl_width=50,
            fixed_form_width=150
        )
        #
        # Creating layout and widgets to display planet orbit stats
        #
        stats_layout = QtWidgets.QGridLayout()
        self.stats_components: list[ValueViewer] = []
        for i, orbit_stat in enumerate(OrbitsPage.ORBITS_STATS.keys()):
            stat_name, stat_value = orbit_stat, OrbitsPage.ORBITS_STATS[orbit_stat]
            stats_component = ValueViewer(stat_name,
                                          stat_value,
                                          fixed_width=150,
                                          fixed_key_height=20,
                                          fixed_value_height=35,
                                          alignment=QtCore.Qt.AlignmentFlag.AlignTop)
            self.stats_components.append(stats_component)
            stats_layout.addLayout(stats_component, i // 2, i % 2, 1, 1)
        #
        # Appending these widgets to a wrapper layout
        #
        controls_layout = QtWidgets.QVBoxLayout()
        controls_layout.addStretch()
        controls_layout.addLayout(planet_picker_layout)
        controls_layout.addSpacing(10)
        controls_layout.addLayout(stats_layout)
        controls_layout.addStretch()
        controls_layout.setContentsMargins(10, 10, 10, 10)
        root_layout.addLayout(controls_layout)
        #
        # Displaying the root layout containing all the widgets of the orbit page
        #
        self.setLayout(root_layout)

    def on_planet_dropdown_changed(self, new_index: int):
        new_planet: str = PLANETS[new_index]
        print("NEW PLANET: ", new_planet)
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
            SettingsKeys.ORBIT_TIME.value: 1,
            SettingsKeys.VIEW_TYPE.value: ViewType.TWO_D.value
        }
        root_layout = QtWidgets.QVBoxLayout()
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        reset_button = QtWidgets.QPushButton("Reset")
        reset_button.clicked.connect(self.on_reset_button_pressed)
        reset_button.setFixedWidth(150)
        back_button = QtWidgets.QPushButton("Back")
        back_button.clicked.connect(self.on_back_button_pressed)
        back_button.setFixedWidth(150)
        button_layout.addWidget(reset_button)
        button_layout.addWidget(back_button)
        button_layout.addStretch()
        root_layout.addLayout(button_layout)
        self.controls_layout = QtWidgets.QVBoxLayout()
        self.init_settings_widgets()
        root_layout.addLayout(self.controls_layout)
        self.setLayout(root_layout)

    def on_reset_button_pressed(self):
        if self.settings.SETTINGS != self.original_settings:
            for k in self.original_settings.keys():
                self.settings.SETTINGS[k] = self.original_settings[k]
            self.centre_of_orbit_picker.set_value(self.settings.SETTINGS[SettingsKeys.CENTRE_OF_ORBIT.value])
            self.objects_to_show.set_value(self.settings.SETTINGS[SettingsKeys.OBJECTS_TO_SHOW.value])
            for widget in self.child_widgets:
                widget.set_state()

    def on_back_button_pressed(self):
        self.parent.switch_to(PageIndexes.ORBITS_PAGE.value, post_func=lambda w: w.update_graph())

    def init_settings_widgets(self):
        top_half = QtWidgets.QHBoxLayout()
        top_half.addStretch()
        # centre_of_orbit_picker = CentreOfOrbitPicker(self.settings,
        #                                              margin=[10, 10, 10, 10])
        # self.child_widgets.append(centre_of_orbit_picker)
        # top_half.addLayout(centre_of_orbit_picker)
        self.centre_of_orbit_picker = VerticalValuePicker(value_type="from_multiple",
                                                          lbl_text="Centre of orbit: ",
                                                          fixed_lbl_height=20,
                                                          choices=["Sun"] + PLANETS,
                                                          padding=[10, 10, 10, 10],
                                                          on_change=self.on_centre_of_orbit_changed)
        self.centre_of_orbit_picker.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.centre_of_orbit_picker.set_value(self.settings.SETTINGS[SettingsKeys.CENTRE_OF_ORBIT.value])
        top_half.addLayout(self.centre_of_orbit_picker)
        # objects_to_show = ObjToShowCheckboxGroup(self.settings,
        #                                          OrbitsPageSettings.OBJECTS_TO_SHOW_OPTIONS,
        #                                          margin=[10, 10, 10, 10])
        # self.child_widgets += objects_to_show.check_boxes
        # top_half.addLayout(objects_to_show)
        self.objects_to_show = VerticalValuePicker(value_type="many_from_multiple",
                                                   lbl_text="Objects to show: ",
                                                   choices=["Sun"] + PLANETS,
                                                   padding=[10, 10, 10, 10],
                                                   fixed_lbl_height=20,
                                                   on_change=self.on_object_to_show_checkbox_changed)
        self.objects_to_show.set_value(self.settings.SETTINGS[SettingsKeys.OBJECTS_TO_SHOW.value])
        self.objects_to_show.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        top_half.addLayout(self.objects_to_show)
        top_half.addStretch()
        self.controls_layout.addLayout(top_half)
        bottom_half = QtWidgets.QHBoxLayout()
        bottom_half.addStretch()
        view_type_picker = ViewTypePicker(self.settings,
                                          margin=[10, 10, 10, 10],
                                          alignment=QtCore.Qt.AlignmentFlag.AlignTop)
        self.child_widgets.append(view_type_picker)
        bottom_half.addLayout(view_type_picker)
        orbit_time_picker = OrbitTimePicker(self.settings,
                                            fixed_width=150,
                                            alignment=QtCore.Qt.AlignmentFlag.AlignTop,
                                            margin=[10, 10, 10, 10])
        self.child_widgets.append(orbit_time_picker)
        bottom_half.addLayout(orbit_time_picker)
        bottom_half.addStretch()
        bottom_half.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.controls_layout.addLayout(bottom_half)
        self.controls_layout.setStretch(0, 0)
        self.controls_layout.setStretch(1, 1)

    def on_centre_of_orbit_changed(self, new_index: int):
        self.settings.SETTINGS[SettingsKeys.CENTRE_OF_ORBIT.value] = self.centre_of_orbit_picker.choices[new_index]

    def on_object_to_show_checkbox_changed(self, checkbox: QtWidgets.QCheckBox):
        k = SettingsKeys.OBJECTS_TO_SHOW.value
        objects_to_show = self.settings.SETTINGS[k]
        if checkbox.isChecked():
            objects_to_show.append(checkbox.text())
        else:
            objects_to_show.remove(checkbox.text())
        self.settings.SETTINGS[k] = list(set(objects_to_show))


class SpirographPage(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setParent(parent)
        root_layout = QtWidgets.QHBoxLayout()
        self.sim_settings = OrbitSimSettings()
        # self.figure_canvas = FigureCanvas(self)
        # self.figure_canvas.plot([0, 1, 2, 3, 4], [10, 1, 20, 3, 40])
        graph_layout = QtWidgets.QVBoxLayout()
        # toolbar = NavigationToolbar(self.figure_canvas, self)
        # graph_layout.addWidget(toolbar)
        # graph_layout.addWidget(self.figure_canvas)
        root_layout.addLayout(graph_layout)
        controls_layout = QtWidgets.QVBoxLayout()
        self.planet1picker: HorizontalValuePicker = HorizontalValuePicker(
            value_type="from_multiple",
            lbl_text="Planet 1: ",
            default_val="Venus",
            choices=PLANETS,
            padding=[5, 5, 5, 5]
        )
        self.planet2picker: HorizontalValuePicker = HorizontalValuePicker(
            value_type="from_multiple",
            lbl_text="Planet 2: ",
            default_val="Earth",
            choices=PLANETS,
            padding=[5, 5, 5, 5]
        )
        self.time_diff_picker: HorizontalValuePicker = HorizontalValuePicker(
            value_type=float,
            lbl_text="Δt: ",
            tooltip="The time difference between drawing each line",
            fixed_form_width=100,
            fixed_lbl_width=20,
            fixed_height=20,
            padding=[5, 5, 5, 5])
        self.n_orbits: HorizontalValuePicker = HorizontalValuePicker(
            value_type=int,
            lbl_text="N: ",
            tooltip="Number of orbits of the outermost planet",
            fixed_form_width=100,
            fixed_lbl_width=20,
            fixed_height=20)

        param_picker_layout = QtWidgets.QVBoxLayout()
        planet_picker_layout = QtWidgets.QHBoxLayout()
        planet_picker_layout.addLayout(self.planet1picker)
        planet_picker_layout.addLayout(self.planet2picker)
        param_picker_layout.addLayout(planet_picker_layout)
        num_picker_layout = QtWidgets.QHBoxLayout()
        num_picker_layout.addLayout(self.time_diff_picker)
        num_picker_layout.addLayout(self.n_orbits)
        param_picker_layout.addLayout(num_picker_layout)
        param_picker_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        controls_layout.addStretch()
        controls_layout.addLayout(param_picker_layout)
        eval_button = QtWidgets.QPushButton("Evaluate")
        eval_button.pressed.connect(self.on_eval_button_press)
        controls_layout.addSpacing(20)
        controls_layout.addWidget(eval_button)
        values_layout = QtWidgets.QHBoxLayout()
        self.completed_orbits = ValueViewer("Completed orbits",
                                            fixed_key_height=20,
                                            fixed_value_height=50,
                                            fixed_width=120,
                                            alignment=QtCore.Qt.AlignmentFlag.AlignTop)
        self.elapsed_time = ValueViewer("Elapsed time",
                                        fixed_key_height=20,
                                        fixed_value_height=50,
                                        fixed_width=120,
                                        alignment=QtCore.Qt.AlignmentFlag.AlignTop)
        values_layout.addLayout(self.completed_orbits)
        values_layout.addLayout(self.elapsed_time)
        values_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        controls_layout.addSpacing(20)
        controls_layout.addLayout(values_layout)
        controls_layout.addStretch()
        root_layout.addLayout(controls_layout)
        self.setLayout(root_layout)

    def on_eval_button_press(self):
        print(self.planet1picker.get_value(),
              self.planet2picker.get_value(),
              self.time_diff_picker.get_value(),
              self.n_orbits.get_value())
        # TODO: integrate functionality to plot spirograph based on input parameters


class PageClasses(Enum):
    ORBITS_PAGE = OrbitsPage
    ORBITS_PAGE_SETTINGS = OrbitsPageSettings
    SPIROGRAPH_PAGE = SpirographPage
