from PyQt6 import QtCore, QtGui, QtWidgets
from enum import Enum

PLANETS: list[str] = ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]


class SettingsKeys(Enum):
    CENTRE_OF_ORBIT = "Centre of orbit"
    OBJECTS_TO_SHOW = "Objects to show"
    ANIM_SPEED = "Animation Speed"
    ORBIT_TIME = "Orbit time"
    VIEW_TYPE = "View type"


class ViewType(Enum):
    TWO_D = "2D"
    THREE_D = "3D"


class OrbitSimSettings:
    SETTINGS: dict = {
        SettingsKeys.CENTRE_OF_ORBIT.value: "Sun",
        SettingsKeys.OBJECTS_TO_SHOW.value: ["Sun"] + PLANETS,
        SettingsKeys.ANIM_SPEED.value: 1,
        SettingsKeys.ORBIT_TIME.value: 1,
        SettingsKeys.VIEW_TYPE.value: ViewType.TWO_D.value
    }


class ObjToShowCheckbox(QtWidgets.QCheckBox):
    def __init__(self, settings: OrbitSimSettings, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.settings: OrbitSimSettings = settings
        self.settings_key: str = SettingsKeys.OBJECTS_TO_SHOW.value
        self.set_state()
        self.toggled.connect(self.update_obj_to_show)

    def update_obj_to_show(self):
        if self.isChecked():
            self.settings.SETTINGS[self.settings_key].append(self.text())
        else:
            self.settings.SETTINGS[self.settings_key].remove(self.text())
        self.settings.SETTINGS[self.settings_key] = list(set(self.settings.SETTINGS[self.settings_key]))

    def set_state(self):
        self.setChecked(self.text() in self.settings.SETTINGS[self.settings_key])


class CentreOfOrbitPicker(QtWidgets.QVBoxLayout):
    __OPTIONS: list[str] = ["Sun"] + PLANETS

    def __init__(self, settings, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.settings: OrbitSimSettings = settings
        self.settings_key: str = SettingsKeys.CENTRE_OF_ORBIT.value
        self.addWidget(QtWidgets.QLabel("Centre of orbit"))
        self.combo_box: QtWidgets.QComboBox = QtWidgets.QComboBox()
        self.combo_box.addItems(CentreOfOrbitPicker.__OPTIONS)
        self.set_state()
        self.combo_box.currentIndexChanged.connect(self.update_centre_of_orbit)
        self.addWidget(self.combo_box)

    def update_centre_of_orbit(self, new_index: int):
        self.settings.SETTINGS[self.settings_key] = CentreOfOrbitPicker.__OPTIONS[new_index]

    def set_state(self):
        self.combo_box.setCurrentIndex(CentreOfOrbitPicker.__OPTIONS.index(self.settings.SETTINGS[self.settings_key]))


class AnimSpeedPicker(QtWidgets.QVBoxLayout):
    __MIN_VAL: int = 0
    __MAX_VAL: int = 10
    __TICK_INTERVAL: int = 1

    def __init__(self, settings: OrbitSimSettings, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.settings: OrbitSimSettings = settings
        self.settings_key: str = SettingsKeys.ANIM_SPEED.value
        self.addWidget(QtWidgets.QLabel("Animation speed"))
        self.anim_speed_slider: QtWidgets.QSlider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.anim_speed_slider.setMinimum(AnimSpeedPicker.__MIN_VAL)
        self.anim_speed_slider.setMaximum(AnimSpeedPicker.__MAX_VAL)
        assert AnimSpeedPicker.__MIN_VAL <= self.settings.SETTINGS[self.settings_key] <= AnimSpeedPicker.__MAX_VAL
        self.set_state()
        self.anim_speed_slider.setTickInterval(AnimSpeedPicker.__TICK_INTERVAL)
        self.anim_speed_slider.setTickPosition(QtWidgets.QSlider.TickPosition.TicksBelow)
        self.anim_speed_slider.valueChanged.connect(self.update_anim_speed)
        self.addWidget(self.anim_speed_slider)
        self.anim_speed_indicator: QtWidgets.QLabel = QtWidgets.QLabel(f"{self.anim_speed_slider.value()}x")
        self.addWidget(self.anim_speed_indicator)

    def update_anim_speed(self, new_value: int):
        self.settings.SETTINGS[self.settings_key] = new_value
        self.anim_speed_indicator.setText(f"{new_value}x")

    def set_state(self):
        self.anim_speed_slider.setValue(self.settings.SETTINGS[self.settings_key])


class ViewTypePicker(QtWidgets.QVBoxLayout):
    def __init__(self, settings: OrbitSimSettings, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.settings: OrbitSimSettings = settings
        self.settings_key: str = SettingsKeys.VIEW_TYPE.value
        self.addWidget(QtWidgets.QLabel("View type"))
        self.view_type_btn_layout = QtWidgets.QHBoxLayout()
        self._2d_view_type_btn = QtWidgets.QRadioButton(ViewType.TWO_D.value)
        self._3d_view_type_btn = QtWidgets.QRadioButton(ViewType.THREE_D.value)
        self.set_state()
        self._2d_view_type_btn.toggled.connect(self._2d_view_type_toggled)
        self._3d_view_type_btn.toggled.connect(self._3d_view_type_toggled)
        self.view_type_btn_layout.addWidget(self._2d_view_type_btn)
        self.view_type_btn_layout.addWidget(self._3d_view_type_btn)
        self.addLayout(self.view_type_btn_layout)

    def _2d_view_type_toggled(self):
        self._3d_view_type_btn.setChecked(False)
        self.settings.SETTINGS[self.settings_key] = ViewType.TWO_D.value

    def _3d_view_type_toggled(self):
        self._2d_view_type_btn.setChecked(False)
        self.settings.SETTINGS[self.settings_key] = ViewType.THREE_D.value

    def set_state(self):
        self._2d_view_type_btn.setChecked(self.settings.SETTINGS[self.settings_key] == ViewType.TWO_D.value)


class OrbitTimePicker(QtWidgets.QVBoxLayout):
    __MIN_VAL: int = 1
    __MAX_VAL: int = 10
    __TICK_INTERVAL: int = 1

    def __init__(self, settings: OrbitSimSettings, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.settings: OrbitSimSettings = settings
        self.settings_key: str = SettingsKeys.ORBIT_TIME.value
        self.addWidget(QtWidgets.QLabel("Orbit time (for shortest orbit)"))
        self.orbit_time_slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.orbit_time_slider.setMinimum(OrbitTimePicker.__MIN_VAL)
        self.orbit_time_slider.setMaximum(OrbitTimePicker.__MAX_VAL)
        self.set_state()
        self.orbit_time_slider.setTickPosition(QtWidgets.QSlider.TickPosition.TicksBelow)
        self.orbit_time_slider.setTickInterval(OrbitTimePicker.__TICK_INTERVAL)
        self.orbit_time_slider.valueChanged.connect(self.update_orbit_time)
        self.addWidget(self.orbit_time_slider)
        self.orbit_time_indicator = QtWidgets.QLabel(f"{self.orbit_time_slider.value()} s")
        self.addWidget(self.orbit_time_indicator)

    def update_orbit_time(self, new_value: int):
        self.settings.SETTINGS[self.settings_key] = new_value
        self.orbit_time_indicator.setText(f"{self.orbit_time_slider.value()} s")

    def set_state(self):
        self.orbit_time_slider.setValue(self.settings.SETTINGS[self.settings_key])
