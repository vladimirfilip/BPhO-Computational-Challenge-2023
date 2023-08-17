from typing import Optional
from PyQt6 import QtCore, QtGui, QtWidgets
from enum import Enum

from _decimal import Decimal
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from math import cos, sqrt, pi

from backend._2d_animation import Animation2D
from backend._3d_animation import Animation3D
from ui.components import OrbitSimSettings, ViewTypePicker, SettingsKeys, ViewType, SettingsBtnLayout, \
    HorizontalValuePicker, ValueViewer, VerticalValuePicker, StarSystem, solar_system_enum_to_class
import matplotlib

from backend.spiro_animation import SpiroAnimation

matplotlib.use('TkAgg')

PLANETS: list[str] = ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"]


class PageIndexes(Enum):
    ORBITS_PAGE = 0
    ORBITS_PAGE_SETTINGS = 1
    SPIROGRAPH_PAGE = 2


class OrbitsPage(QtWidgets.QWidget):
    #
    # Dictionary storing the name and value of the orbit statistics displayed
    #
    ORBITS_STATS: dict[str, Optional[str]] = {
        "Coordinates": None,
        "Mass": None,
        "Angular velocity": None,
        "Linear velocity": None,
        "Distance from centre": None,
        "Distance from star": None,
        "Orbital angle": None,
        "Eccentricity": None,
        "Semi-major axis": None,
        "Semi-minor axis": None,
        "Orbital period": None,
        "Inclination angle": None,
    }

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setParent(parent)
        root_layout = QtWidgets.QHBoxLayout()
        #
        # Initialises simulation settings class with default settings
        #
        self.sim_settings = OrbitSimSettings()
        #
        # Creating the graph canvas and the toolbar to manipulate it
        #
        self.fig = Figure(figsize=(12, 12), dpi=100)
        self.canvas = FigureCanvas(self.fig)
        self.graph_layout = QtWidgets.QVBoxLayout()
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.graph_layout.addWidget(self.toolbar)
        self.graph_layout.addWidget(self.canvas)
        settings_btn_layout = SettingsBtnLayout(on_click=self.on_settings_button_click,
                                                btn_width=30,
                                                btn_height=30)
        self.graph_layout.addLayout(settings_btn_layout)
        root_layout.addLayout(self.graph_layout)
        self.anim = None
        self.display_animation()
        #
        # Creating layout and widgets for user to pick planet to see orbit stats on
        #
        self.planet_picker_layout = HorizontalValuePicker(
            lbl_text="Planet: ",
            value_type="from_multiple",
            default_val="Earth",
            choices=PLANETS,
            tooltip="Choose the name of the planet to see orbit stats on",
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
                                          alignment=QtCore.Qt.AlignmentFlag.AlignTop)
            stats_component.label.setWordWrap(True)
            self.stats_components.append(stats_component)
            stats_layout.addLayout(stats_component, i // 2, i % 2, 1, 1)
        #
        # Appending these widgets to a wrapper layout
        #
        controls_layout = QtWidgets.QVBoxLayout()
        controls_layout.addStretch()
        controls_layout.addLayout(self.planet_picker_layout)
        controls_layout.addSpacing(10)
        controls_layout.addLayout(stats_layout)
        controls_layout.addStretch()
        controls_layout.setContentsMargins(10, 10, 10, 10)
        root_layout.addLayout(controls_layout)
        #
        # Displaying the root layout containing all the widgets of the orbit page
        #
        self.setLayout(root_layout)

    def on_settings_button_click(self):
        self.parent.switch_to(PageIndexes.ORBITS_PAGE_SETTINGS.value)

    def update_graph(self):
        #
        # Called when simulation settings have been updated
        # Updates planet picker so that only statistics on the planets being animated can be retrieved
        # and re-initialises the animation so that it runs according to the new simulation parameters
        #
        self.planet_picker_layout.set_choices(self.sim_settings.SETTINGS[SettingsKeys.OBJECTS_TO_SHOW.value], 0)
        self.display_animation()

    def display_animation(self):
        """
        Initialises the animation based on parameters given in settings
        :return: None
        """
        #
        # Retrieves parameters from settings class
        #
        settings = self.sim_settings.SETTINGS
        solar_system = settings[SettingsKeys.STAR_SYSTEM.value]
        solar_system_class = solar_system_enum_to_class[solar_system]
        centre = solar_system_class.Planet(settings[SettingsKeys.CENTRE_OF_ORBIT.value]).name
        planets = [solar_system_class.Planet(s).name for s in settings[SettingsKeys.OBJECTS_TO_SHOW.value]]
        orbit_duration = int(settings[SettingsKeys.ORBIT_TIME.value])
        num_orbits = int(settings[SettingsKeys.NUM_ORBITS.value])
        #
        # Deletes the old canvas and toolbar and creates new ones
        #
        if self.anim:
            self.anim.ani.event_source.stop()
        self.graph_layout.removeWidget(self.canvas)
        self.graph_layout.removeWidget(self.toolbar)
        self.fig = Figure(figsize=(10, 10))
        self.canvas = FigureCanvas(self.fig)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.graph_layout.insertWidget(0, self.toolbar)
        self.graph_layout.insertWidget(1, self.canvas)
        #
        # Initialises the new animation from arguments
        #
        args = [self.fig, solar_system.name, planets, centre, orbit_duration, num_orbits, self.refresh_stats_labels]
        animation_class = Animation2D if settings[SettingsKeys.VIEW_TYPE.value] == ViewType.TWO_D.value else Animation3D
        self.anim = animation_class(*args)

    def refresh_stats_labels(self, theta_angles: list[float], coords: list[list[float]]):
        """
        Refreshes the contents of the statistics labels. This function is called after every frame
        :param theta_angles: the current orbital angles of all the planets in the animation
        :param coords: the coordinates of all the planets in the animation
        :return: None, labels are modified in-place
        """
        #
        # Calculates which star system and planet to show statistics on
        #
        i = self.planet_picker_layout.form.currentIndex()
        planet_name = self.planet_picker_layout.choices[i]
        solar_system = self.sim_settings.SETTINGS[SettingsKeys.STAR_SYSTEM.value]
        solar_system_class = solar_system_enum_to_class[solar_system]
        try:
            if planet_name == solar_system_class.SUN:
                planet_enum_key = solar_system_class.Planet(
                    self.sim_settings.SETTINGS[SettingsKeys.CENTRE_OF_ORBIT.value]).name
            else:
                planet_enum_key = solar_system_class.Planet(planet_name).name
        except ValueError:
            # star system is being actively changed in settings, and so refreshing is paused until everything is synced
            return
        #
        # Retrieves key constants from the relevant constant enum classes
        #
        star_enum_key = solar_system_class.SUN
        earth_mass = Decimal('5.972') * Decimal(Decimal('10') ** Decimal('24'))
        au_in_metres = Decimal('1.496') * Decimal(Decimal('10') ** Decimal('11'))
        G: Decimal = Decimal('6.67') * Decimal(Decimal('10') ** Decimal('-11'))
        M: Decimal = solar_system_class.Mass[star_enum_key].value * earth_mass
        e: Decimal = solar_system_class.Eccentricity[planet_enum_key].value
        b: Decimal = solar_system_class.SemiMinorAxis[planet_enum_key].value * au_in_metres
        a: Decimal = solar_system_class.SemiMajorAxis[planet_enum_key].value * au_in_metres
        m: Decimal = solar_system_class.Mass[planet_enum_key].value * earth_mass
        P: Decimal = solar_system_class.OrbitalPeriod[planet_enum_key].value
        beta: Decimal = solar_system_class.InclinationAngle[planet_enum_key].value
        #
        # Retrieves orbital angle and coordinates from the data received from the animation class
        #
        theta: float = theta_angles[i] % float(Decimal('2') * Decimal(pi))
        coords: list[float] = coords[i]
        #
        # Calculates orbital radius, linear velocity and angular velocity (relative to the star), using these constants
        #
        r = b / (Decimal('1') - e * Decimal(cos(theta)))
        if a == 0:
            v = 0
        else:
            v = sqrt(G * M * (Decimal('2') / r - Decimal('1') / a))
        if r == 0:
            w = 0
        else:
            w = Decimal(v) / r
        #
        # Rounds these values, adds units and sets text of the relevant labels to these new statistics
        #
        OrbitsPage.ORBITS_STATS = {
            "Coordinates": ",\n".join([str(round(coord, 6)) + " a.u." for coord in coords]),
            "Mass": f"{round(float(m), 6)} kg",
            "Angular velocity": f"{round(w, 10)} m/s",
            "Linear velocity": f"{round(v, 6)} m/s",
            "Distance from centre": f"{round(sqrt(sum(n * n for n in coords)), 6)} a.u.",
            "Distance from star": f"{round(float(r / au_in_metres), 6)} a.u.",
            "Orbital angle": f"{round(theta, 6)} rad",
            "Eccentricity": e,
            "Semi-major axis": f"{round(a / au_in_metres, 6)} a.u.",
            "Semi-minor axis": f"{round(b / au_in_metres, 6)} a.u.",
            "Orbital period": f"{round(float(P), 6)} years",
            "Inclination angle": f"{round(float(beta), 6)} rad"
        }

        for i, k in enumerate(OrbitsPage.ORBITS_STATS.keys()):
            self.stats_components[i].set_text(OrbitsPage.ORBITS_STATS[k])


class OrbitsPageSettings(QtWidgets.QWidget):
    OBJECTS_TO_SHOW_OPTIONS: list[str]
    CENTRE_OF_ORBIT_OPTIONS: list[str]
    PLANET_STAT_OPTIONS: list[str]

    def __init__(self, parent):
        super().__init__()
        self.child_widgets = []
        self.parent = parent
        self.settings = OrbitSimSettings()
        #
        # Original settings are hard-coded so that the widget knows what the original settings are in case the rest button is pressed
        #
        self.original_settings: dict = {
            SettingsKeys.STAR_SYSTEM.value: StarSystem.SOLAR_SYSTEM,
            SettingsKeys.CENTRE_OF_ORBIT.value: solar_system_enum_to_class[StarSystem.SOLAR_SYSTEM].Planet[solar_system_enum_to_class[StarSystem.SOLAR_SYSTEM].SUN].value,
            SettingsKeys.OBJECTS_TO_SHOW.value: [e.value for e in solar_system_enum_to_class[StarSystem.SOLAR_SYSTEM].Planet if e.name != "SUN"],
            SettingsKeys.ORBIT_TIME.value: 5,
            SettingsKeys.VIEW_TYPE.value: ViewType.TWO_D.value,
            SettingsKeys.NUM_ORBITS.value: 1,
        }
        OrbitsPageSettings.OBJECTS_TO_SHOW_OPTIONS = self.original_settings[SettingsKeys.OBJECTS_TO_SHOW.value]
        OrbitsPageSettings.CENTRE_OF_ORBIT_OPTIONS = [e.value for e in solar_system_enum_to_class[StarSystem.SOLAR_SYSTEM].Planet]
        root_layout = QtWidgets.QVBoxLayout()
        #
        # Appends reset and back buttons to the top of the page
        #
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
        #
        # Initialises the widgets that affect the OrbitSimSettingsClass
        #
        self.controls_layout = QtWidgets.QVBoxLayout()
        self.init_settings_widgets()
        root_layout.addLayout(self.controls_layout)
        self.setLayout(root_layout)

    def on_reset_button_pressed(self):
        """
        Called when the reset button is pressed, resets the state of all widgets according to the parameters in self.original_settings
        :return: None, all widgets are edited in-place
        """
        if self.settings.SETTINGS != self.original_settings:
            for k in self.original_settings.keys():
                self.settings.SETTINGS[k] = self.original_settings[k]
            self.star_system_picker.set_value(self.settings.SETTINGS[SettingsKeys.STAR_SYSTEM.value].value)
            self.centre_of_orbit_picker.set_choices(OrbitsPageSettings.CENTRE_OF_ORBIT_OPTIONS, 0)
            self.objects_to_show.set_value(self.settings.SETTINGS[SettingsKeys.OBJECTS_TO_SHOW.value])
            self.orbit_time_picker.set_value(self.settings.SETTINGS[SettingsKeys.ORBIT_TIME.value])
            self.num_orbits_picker.set_value(self.settings.SETTINGS[SettingsKeys.NUM_ORBITS.value])
            for widget in self.child_widgets:
                widget.set_state()

    def on_back_button_pressed(self):
        #
        # Returns to the orbit page when back button is pressed and calls its update_graph() function to re-render the animation
        #
        self.parent.switch_to(PageIndexes.ORBITS_PAGE.value, post_func=lambda w: w.update_graph())

    def init_settings_widgets(self):
        """
        Initialises each widget one by one, setting bindings and other UI properties
        :return: None
        """
        top_half = QtWidgets.QHBoxLayout()
        top_half.addStretch()
        self.star_system_picker = VerticalValuePicker(value_type="from_multiple",
                                                      lbl_text="Star system: ",
                                                      default_val="Solar System",
                                                      fixed_lbl_height=20,
                                                      choices=[k.value for k in solar_system_enum_to_class.keys()],
                                                      padding=[10, 10, 10, 10],
                                                      on_change=self.on_star_system_changed)
        self.star_system_picker.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        top_half.addLayout(self.star_system_picker)
        self.centre_of_orbit_picker = VerticalValuePicker(value_type="from_multiple",
                                                          lbl_text="Centre of orbit: ",
                                                          fixed_lbl_height=20,
                                                          choices=OrbitsPageSettings.CENTRE_OF_ORBIT_OPTIONS,
                                                          padding=[10, 10, 10, 10],
                                                          on_change=self.on_centre_of_orbit_changed)
        self.centre_of_orbit_picker.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.centre_of_orbit_picker.set_value(self.settings.SETTINGS[SettingsKeys.CENTRE_OF_ORBIT.value])
        top_half.addLayout(self.centre_of_orbit_picker)
        self.objects_to_show = VerticalValuePicker(value_type="many_from_multiple",
                                                   lbl_text="Objects to show: ",
                                                   choices=OrbitsPageSettings.OBJECTS_TO_SHOW_OPTIONS,
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
        self.orbit_time_picker = VerticalValuePicker(value_type=int,
                                                     lbl_text="Orbit time (s): ",
                                                     fixed_width=100,
                                                     tooltip="Orbit time for the longest orbit in seconds",
                                                     fixed_form_height=30,
                                                     padding=[10, 10, 10, 10],
                                                     on_change=self.on_orbit_time_changed)
        self.orbit_time_picker.set_value(self.settings.SETTINGS[SettingsKeys.ORBIT_TIME.value])
        bottom_half.addLayout(self.orbit_time_picker)
        self.num_orbits_picker = VerticalValuePicker(value_type=int,
                                                     lbl_text="Number of orbits: ",
                                                     fixed_width=150,
                                                     tooltip="Number of orbits of the outermost planet",
                                                     fixed_form_height=30,
                                                     padding=[10, 10, 10, 10],
                                                     on_change=self.on_num_orbits_changed)
        self.num_orbits_picker.set_value(self.settings.SETTINGS[SettingsKeys.NUM_ORBITS.value])
        bottom_half.addLayout(self.num_orbits_picker)
        bottom_half.addStretch()
        bottom_half.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.controls_layout.addLayout(bottom_half)
        #
        # Fixes both rows of the page to the top of the window
        #
        self.controls_layout.setStretch(0, 0)
        self.controls_layout.setStretch(1, 1)

    def on_centre_of_orbit_changed(self, new_index: int):
        """
        Called when a new item is chosen in the "Centre of orbit" dropdown. As that new object is the new centre, it should not be animated.
        Therefore, the "Objects to show" dropdown is then updated to include the previous centre object and remove the new one.
        :param new_index: the index of the chosen item
        :return: None
        """
        if new_index < 0 or not self.centre_of_orbit_picker.choices:
            return
        centre_name = self.centre_of_orbit_picker.choices[new_index]
        self.settings.SETTINGS[SettingsKeys.CENTRE_OF_ORBIT.value] = centre_name
        new_objects_to_show_options = [e.value for e in solar_system_enum_to_class[self.settings.SETTINGS[SettingsKeys.STAR_SYSTEM.value]].Planet]
        if centre_name in new_objects_to_show_options:
            new_objects_to_show_options.remove(centre_name)
        OrbitsPageSettings.OBJECTS_TO_SHOW_OPTIONS = new_objects_to_show_options
        self.objects_to_show.set_choices(new_objects_to_show_options)

    def on_object_to_show_checkbox_changed(self, checkboxes: list[QtWidgets.QCheckBox]):
        k = SettingsKeys.OBJECTS_TO_SHOW.value
        self.settings.SETTINGS[k] = [checkbox.text() for checkbox in checkboxes if checkbox.isChecked()]

    def on_orbit_time_changed(self, new_value: int):
        self.settings.SETTINGS[SettingsKeys.ORBIT_TIME.value] = new_value

    def on_num_orbits_changed(self, new_value: int):
        self.settings.SETTINGS[SettingsKeys.NUM_ORBITS.value] = new_value

    def on_star_system_changed(self, new_index: int):
        """
        Called when a star system has been chosen from the dropdown.
        This function has to also update the "centre of orbit" and "objects to show" widgets to present the objects that are in the new star system.
        :param new_index: index of the star system chosen out of the dropdown's items
        :return: None
        """
        star_system: StarSystem = list(solar_system_enum_to_class.keys())[new_index]
        star_system_class = solar_system_enum_to_class[star_system]
        sun_name = star_system_class.Planet[star_system_class.SUN].value
        self.settings.SETTINGS[SettingsKeys.STAR_SYSTEM.value] = star_system
        self.settings.SETTINGS[SettingsKeys.CENTRE_OF_ORBIT.value] = sun_name
        new_objects_to_show = [e.value for e in star_system_class.Planet if e.name != star_system_class.SUN]
        OrbitsPageSettings.OBJECTS_TO_SHOW_OPTIONS = new_objects_to_show
        self.settings.SETTINGS[SettingsKeys.OBJECTS_TO_SHOW.value] = new_objects_to_show
        self.objects_to_show.set_choices(new_objects_to_show, check_all=True)
        OrbitsPageSettings.CENTRE_OF_ORBIT_OPTIONS = [e.value for e in star_system_class.Planet]
        self.centre_of_orbit_picker.set_choices(OrbitsPageSettings.CENTRE_OF_ORBIT_OPTIONS,
                                                0)


class SpirographPage(QtWidgets.QWidget):
    STAR_SYSTEM_OPTIONS = [k.value for k in solar_system_enum_to_class.keys()]
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setParent(parent)
        root_layout = QtWidgets.QHBoxLayout()
        self.sim_settings = OrbitSimSettings()
        self.fig = Figure(figsize=(10, 10))
        self.canvas = FigureCanvas(self.fig)
        self.graph_layout = QtWidgets.QVBoxLayout()
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.graph_layout.addWidget(self.toolbar)
        self.graph_layout.addWidget(self.canvas)
        self.anim = None
        root_layout.addLayout(self.graph_layout)
        controls_layout = QtWidgets.QVBoxLayout()
        controls_layout.addStretch()
        star_system_layout = QtWidgets.QHBoxLayout()
        self.star_system_picker = HorizontalValuePicker(
            value_type="from_multiple",
            lbl_text="Star System: ",
            default_val="Solar System",
            choices=SpirographPage.STAR_SYSTEM_OPTIONS,
            fixed_height=30,
            fixed_lbl_width=90,
            fixed_form_width=120,
            on_change=self.on_star_system_changed
        )
        #self.star_system_picker.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        star_system_layout.addLayout(self.star_system_picker)
        #star_system_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        controls_layout.addLayout(star_system_layout)
        param_picker_layout = QtWidgets.QVBoxLayout()
        planet_picker_layout = QtWidgets.QHBoxLayout()
        planet_picker_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.planet1picker: HorizontalValuePicker = HorizontalValuePicker(
            value_type="from_multiple",
            lbl_text="Planet 1: ",
            fixed_lbl_width=75,
            fixed_form_width=100,
            default_val="Venus",
            choices=PLANETS,
            padding=[5, 5, 5, 5]
        )
        self.planet2picker: HorizontalValuePicker = HorizontalValuePicker(
            value_type="from_multiple",
            lbl_text="Planet 2: ",
            fixed_lbl_width=75,
            fixed_form_width=100,
            default_val="Earth",
            choices=PLANETS,
            padding=[5, 5, 5, 5]
        )
        planet_picker_layout.addLayout(self.planet1picker)
        planet_picker_layout.addLayout(self.planet2picker)
        param_picker_layout.addLayout(planet_picker_layout)
        num_picker_layout = QtWidgets.QHBoxLayout()
        self.speed_picker: HorizontalValuePicker = HorizontalValuePicker(
            value_type="from_multiple",
            lbl_text="Speed: ",
            tooltip="The speed at which a new line is drawn",
            choices=["slow", "medium", "fast"],
            default_val="fast",
            fixed_form_width=75,
            fixed_lbl_width=60,
            fixed_height=25,
            padding=[5, 5, 5, 5])
        self.n_orbits: HorizontalValuePicker = HorizontalValuePicker(
            value_type=int,
            lbl_text="N: ",
            tooltip="Number of orbits of the outermost planet",
            default_val=10,
            fixed_form_width=100,
            fixed_lbl_width=20,
            fixed_height=25,
            padding=[5, 5, 5, 5])
        num_picker_layout.addLayout(self.speed_picker)
        num_picker_layout.addLayout(self.n_orbits)
        param_picker_layout.addLayout(num_picker_layout)
        #param_picker_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        controls_layout.addLayout(param_picker_layout)
        controls_layout.addSpacing(20)
        eval_button_layout = QtWidgets.QHBoxLayout()
        eval_button = QtWidgets.QPushButton("Evaluate")
        eval_button.pressed.connect(self.on_eval_button_press)
        eval_button.setFixedWidth(250)
        eval_button_layout.addWidget(eval_button)
        #eval_button_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        controls_layout.addLayout(eval_button_layout)
        controls_layout.addSpacing(20)
        values_layout = QtWidgets.QHBoxLayout()
        values_layout.addStretch()
        self.completed_orbits = ValueViewer("Completed orbits",
                                            fixed_value_height=50,
                                            fixed_width=100,
                                            alignment=QtCore.Qt.AlignmentFlag.AlignTop)
        self.elapsed_time = ValueViewer("# of lines",
                                        fixed_value_height=50,
                                        fixed_width=80,
                                        alignment=QtCore.Qt.AlignmentFlag.AlignTop)
        values_layout.addLayout(self.completed_orbits)
        values_layout.addLayout(self.elapsed_time)
        values_layout.addStretch()
        values_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        controls_layout.addLayout(values_layout)
        controls_layout.addStretch()
        root_layout.addLayout(controls_layout)
        root_layout.setStretch(1, 0)
        root_layout.setStretch(0, 1)
        self.setLayout(root_layout)
        self.display_animation()

    def on_eval_button_press(self):
        self.display_animation()

    def display_animation(self):
        star_system: StarSystem = StarSystem(self.star_system_picker.get_value())
        star_system_class = solar_system_enum_to_class[star_system]
        planet1: str = star_system_class.Planet(self.planet1picker.get_value()).name
        planet2: str = star_system_class.Planet(self.planet2picker.get_value()).name
        speed: str = self.speed_picker.get_value()
        N: int = int(self.n_orbits.get_value())
        if self.anim:
            self.anim.ani.event_source.stop()
        self.graph_layout.removeWidget(self.canvas)
        self.graph_layout.removeWidget(self.toolbar)
        self.fig = Figure(figsize=(10, 10))
        self.canvas = FigureCanvas(self.fig)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.graph_layout.insertWidget(0, self.toolbar)
        self.graph_layout.insertWidget(1, self.canvas)
        args = [self.fig, star_system.name, planet1, planet2, N, speed, self.refresh_labels]
        self.anim = SpiroAnimation(*args)

    def on_star_system_changed(self, new_index: int):
        if new_index < 0:
            return
        new_star_system_str: str = SpirographPage.STAR_SYSTEM_OPTIONS[new_index]
        new_star_system: StarSystem = StarSystem(new_star_system_str)
        star_system_class = solar_system_enum_to_class[new_star_system]
        sun_name: str = star_system_class.SUN
        self.planet1picker.set_choices([e.value for e in star_system_class.Planet if e.name != sun_name], 0)
        self.planet2picker.set_choices([e.value for e in star_system_class.Planet if e.name != sun_name], 1)

    def refresh_labels(self, n_orbits, lines):
        self.completed_orbits.set_text(n_orbits)
        self.elapsed_time.set_text(lines)


class PageClasses(Enum):
    ORBITS_PAGE = OrbitsPage
    ORBITS_PAGE_SETTINGS = OrbitsPageSettings
    SPIROGRAPH_PAGE = SpirographPage
