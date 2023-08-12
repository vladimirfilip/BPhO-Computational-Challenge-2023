from typing import Callable, Optional

from PyQt6 import QtCore, QtGui, QtWidgets
from enum import Enum

PLANETS: list[str] = ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]


class SettingsBtnLayout(QtWidgets.QHBoxLayout):
    def __init__(self, on_click: Callable, *args, **kwargs):
        btn_width = kwargs.pop("btn_width", None)
        super().__init__(*args, **kwargs)
        self.addStretch()
        self.btn = QtWidgets.QPushButton("Settings")
        if btn_width:
            self.btn.setFixedWidth(btn_width)
        self.btn.clicked.connect(on_click)
        self.addWidget(self.btn)


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
        fixed_width = kwargs.pop("fixed_width", None)
        super().__init__(*args, **kwargs)
        self.settings: OrbitSimSettings = settings
        self.settings_key: str = SettingsKeys.OBJECTS_TO_SHOW.value
        self.set_state()
        self.toggled.connect(self.update_obj_to_show)
        if fixed_width:
            self.setFixedWidth(fixed_width)

    def update_obj_to_show(self):
        if self.isChecked():
            self.settings.SETTINGS[self.settings_key].append(self.text())
        else:
            self.settings.SETTINGS[self.settings_key].remove(self.text())
        self.settings.SETTINGS[self.settings_key] = list(set(self.settings.SETTINGS[self.settings_key]))

    def set_state(self):
        self.setChecked(self.text() in self.settings.SETTINGS[self.settings_key])


class ObjToShowCheckboxGroup(QtWidgets.QVBoxLayout):
    def __init__(self, settings: OrbitSimSettings, options: list[str], *args, **kwargs):
        margin = kwargs.pop("margin", None)
        alignment = kwargs.pop("alignment", None)
        fixed_width = kwargs.pop("fixed_width", None)
        super().__init__(*args, **kwargs)
        self.label = QtWidgets.QLabel("Objects to show")
        self.label.setFixedHeight(16)
        self.addWidget(self.label)
        self.check_boxes = []
        for i, option in enumerate(options):
            check_box = ObjToShowCheckbox(settings,
                                          option,
                                          fixed_width=fixed_width)
            self.addWidget(check_box)
            self.check_boxes.append(check_box)
        if alignment:
            self.setAlignment(alignment)
        if margin:
            self.setContentsMargins(*margin)


class CentreOfOrbitPicker(QtWidgets.QVBoxLayout):
    __OPTIONS: list[str] = ["Sun"] + PLANETS

    def __init__(self, settings, *args, **kwargs):
        margin = kwargs.pop("margin", None)
        super().__init__(*args, **kwargs)
        if margin:
            self.setContentsMargins(*margin)

        self.settings: OrbitSimSettings = settings
        self.settings_key: str = SettingsKeys.CENTRE_OF_ORBIT.value
        self.label = QtWidgets.QLabel("Centre of orbit")
        self.label.setFixedWidth(100)
        self.label.setFixedHeight(16)
        self.addWidget(self.label)
        self.combo_box: QtWidgets.QComboBox = QtWidgets.QComboBox()
        self.combo_box.addItems(CentreOfOrbitPicker.__OPTIONS)
        self.combo_box.setFixedWidth(100)
        self.set_state()
        self.combo_box.currentIndexChanged.connect(self.update_centre_of_orbit)
        self.addWidget(self.combo_box)
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

    def update_centre_of_orbit(self, new_index: int):
        self.settings.SETTINGS[self.settings_key] = CentreOfOrbitPicker.__OPTIONS[new_index]

    def set_state(self):
        self.combo_box.setCurrentIndex(CentreOfOrbitPicker.__OPTIONS.index(self.settings.SETTINGS[self.settings_key]))


class AnimSpeedPicker(QtWidgets.QVBoxLayout):
    __MIN_VAL: int = 0
    __MAX_VAL: int = 10
    __TICK_INTERVAL: int = 1

    def __init__(self, settings: OrbitSimSettings, *args, **kwargs):
        alignment = kwargs.pop("alignment", None)
        margins = kwargs.pop("margins", None)
        super().__init__(*args, **kwargs)
        self.settings: OrbitSimSettings = settings
        self.settings_key: str = SettingsKeys.ANIM_SPEED.value
        self.label = QtWidgets.QLabel("Animation speed")
        self.label.setFixedWidth(150)
        self.label.setFixedHeight(16)
        self.addWidget(self.label)
        self.anim_speed_slider: QtWidgets.QSlider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.anim_speed_slider.setMinimum(AnimSpeedPicker.__MIN_VAL)
        self.anim_speed_slider.setMaximum(AnimSpeedPicker.__MAX_VAL)
        self.anim_speed_slider.setFixedWidth(150)
        self.anim_speed_slider.setFixedHeight(30)
        assert AnimSpeedPicker.__MIN_VAL <= self.settings.SETTINGS[self.settings_key] <= AnimSpeedPicker.__MAX_VAL
        self.set_state()
        self.anim_speed_slider.setTickInterval(AnimSpeedPicker.__TICK_INTERVAL)
        self.anim_speed_slider.setTickPosition(QtWidgets.QSlider.TickPosition.TicksBelow)
        self.anim_speed_slider.valueChanged.connect(self.update_anim_speed)
        self.addWidget(self.anim_speed_slider)
        self.anim_speed_indicator: QtWidgets.QLabel = QtWidgets.QLabel(f"{self.anim_speed_slider.value()}x")
        self.addWidget(self.anim_speed_indicator)
        if alignment:
            self.setAlignment(alignment)
        if margins:
            self.setContentsMargins(*margins)

    def update_anim_speed(self, new_value: int):
        self.settings.SETTINGS[self.settings_key] = new_value
        self.anim_speed_indicator.setText(f"{new_value}x")

    def set_state(self):
        self.anim_speed_slider.setValue(self.settings.SETTINGS[self.settings_key])


class ViewTypePicker(QtWidgets.QVBoxLayout):
    def __init__(self, settings: OrbitSimSettings, *args, **kwargs):
        margin = kwargs.pop("margin", None)
        alignment = kwargs.pop("alignment", None)
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
        if margin:
            self.setContentsMargins(*margin)
        if alignment:
            self.setAlignment(alignment)

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
        fixed_width = kwargs.pop("fixed_width", None)
        margin = kwargs.pop("margin", None)
        alignment = kwargs.pop("alignment", None)
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
        if fixed_width:
            self.orbit_time_slider.setFixedWidth(fixed_width)
        self.addWidget(self.orbit_time_slider)
        self.orbit_time_indicator = QtWidgets.QLabel(f"{self.orbit_time_slider.value()} s")
        self.addWidget(self.orbit_time_indicator)
        if margin:
            self.setContentsMargins(*margin)
        if alignment:
            self.setAlignment(alignment)

    def update_orbit_time(self, new_value: int):
        self.settings.SETTINGS[self.settings_key] = new_value
        self.orbit_time_indicator.setText(f"{self.orbit_time_slider.value()} s")

    def set_state(self):
        self.orbit_time_slider.setValue(self.settings.SETTINGS[self.settings_key])


class HorizontalValuePicker(QtWidgets.QHBoxLayout):
    def __init__(self, value_type: type | str, lbl_text: str, default_val=None, choices: Optional[list] = None,
                 tooltip: Optional[str] = None, on_change: Optional[Callable] = None,
                 fixed_lbl_width: Optional[int] = None, fixed_form_width: Optional[int] = None,
                 fixed_height: Optional[int] = None, padding: Optional[list[int]] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label = QtWidgets.QLabel(lbl_text)
        if tooltip:
            self.label.setToolTip(tooltip)
        if fixed_height:
            self.label.setFixedHeight(fixed_height)
        if fixed_lbl_width:
            self.label.setFixedWidth(fixed_lbl_width)
        self.addWidget(self.label)
        if value_type in [int, float, str]:
            self.line_edit = QtWidgets.QLineEdit()
            if value_type == int:
                self.line_edit.setValidator(QtGui.QIntValidator())
            if value_type == float:
                self.line_edit.setValidator(QtGui.QDoubleValidator())
            if default_val:
                self.line_edit.setText(default_val)
            if on_change:
                self.line_edit.textChanged.connect(on_change)
            self.form = self.line_edit
        elif value_type == "from_multiple":
            self.dropdown = QtWidgets.QComboBox()
            assert choices is not None, "a list of choices must be provided when dropdown declared"
            self.choices = choices
            self.dropdown.addItems(choices)
            if default_val:
                assert default_val in choices, "default value given is not present in the possible options"
                self.dropdown.setCurrentIndex(choices.index(default_val))
            if on_change:
                self.dropdown.currentIndexChanged.connect(on_change)
            self.form = self.dropdown
        else:
            raise TypeError("invalid value type for ValuePicker")
        if fixed_form_width:
            self.form.setFixedWidth(fixed_form_width)
        if fixed_height:
            self.form.setFixedHeight(fixed_height)
        if padding:
            self.setContentsMargins(*padding)
        self.addWidget(self.form)

    def get_value(self):
        if isinstance(self.form, QtWidgets.QComboBox):
            return self.choices[self.form.currentIndex()]
        if isinstance(self.form, QtWidgets.QLineEdit):
            return self.form.text()
        raise TypeError("cannot handle form of type {}".format(type(self.form)))


class VerticalValuePicker(QtWidgets.QVBoxLayout):
    def __init__(self, value_type: type | str, lbl_text: str, default_val=None, choices: Optional[list] = None,
                 tooltip: Optional[str] = None, on_change: Optional[Callable] = None,
                 fixed_lbl_height: Optional[int] = None, fixed_form_height: Optional[int] = None,
                 fixed_width: Optional[int] = None, padding: Optional[list[int]] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value_type = value_type
        self.label = QtWidgets.QLabel(lbl_text)
        if tooltip:
            self.label.setToolTip(tooltip)
        if fixed_lbl_height:
            self.label.setFixedHeight(fixed_lbl_height)
        self.addWidget(self.label)
        if value_type in [int, float, str]:
            self.line_edit = QtWidgets.QLineEdit()
            if value_type == int:
                self.line_edit.setValidator(QtGui.QIntValidator())
            if value_type == float:
                self.line_edit.setValidator(QtGui.QDoubleValidator())
            if default_val:
                self.line_edit.setText(default_val)
            if on_change:
                self.line_edit.textChanged.connect(on_change)
            self.form = self.line_edit
        elif value_type == "from_multiple":
            self.dropdown = QtWidgets.QComboBox()
            assert choices is not None, "a list of choices must be provided when dropdown declared"
            self.choices = choices
            self.dropdown.addItems(choices)
            if default_val:
                assert default_val in choices, "default value given is not present in the possible options"
                self.dropdown.setCurrentIndex(choices.index(default_val))
            if on_change:
                self.dropdown.currentIndexChanged.connect(on_change)
            self.form = self.dropdown
        else:
            raise TypeError("invalid value type for ValuePicker")
        if fixed_form_height:
            self.form.setFixedHeight(fixed_form_height)
        if fixed_width:
            self.label.setFixedWidth(fixed_width)
            self.form.setFixedHeight(fixed_width)
        if padding:
            self.setContentsMargins(*padding)
        self.addWidget(self.form)

    def get_value(self):
        if isinstance(self.form, QtWidgets.QComboBox):
            return self.choices[self.form.currentIndex()]
        if isinstance(self.form, QtWidgets.QLineEdit):
            return self.form.text()
        raise TypeError("cannot handle form of type {}".format(type(self.form)))

    def set_choices(self, choices: list, current_index: int):
        self.form.clear()
        self.form.addItems(choices)
        self.form.setCurrentIndex(current_index)

    def set_value(self, new_value):
        if self.value_type in [int, float, str]:
            self.form.setText(new_value)
        elif self.value_type == "from_multiple":
            assert new_value in self.choices, "new value must be from choices available in the dropdown"
            self.form.setCurrentIndex(self.choices.index(new_value))


class ValueViewer(QtWidgets.QVBoxLayout):
    def __init__(self, k: str, v: str = "-", fixed_key_height: Optional[int] = None,
                 fixed_value_height: Optional[int] = None, fixed_width: Optional[int] = None,
                 alignment: Optional[QtCore.Qt.AlignmentFlag] = None, padding: Optional[list[int]] = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.key_label = QtWidgets.QLabel(k)
        self.addWidget(self.key_label)
        if fixed_key_height:
            self.key_label.setFixedHeight(fixed_key_height)
        self.label = QtWidgets.QLabel()
        if fixed_value_height:
            self.label.setFixedHeight(fixed_value_height)
        self.set_text(v)
        self.addWidget(self.label)
        if fixed_width:
            self.label.setFixedWidth(fixed_width)
            self.key_label.setFixedWidth(fixed_width)
        if alignment:
            self.setAlignment(alignment)
        if padding:
            self.setContentsMargins(*padding)

    def set_text(self, new_text: str):
        self.label.setText(new_text if new_text else "-")
