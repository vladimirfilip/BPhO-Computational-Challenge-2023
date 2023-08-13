from typing import Callable, Optional

from PyQt6 import QtCore, QtGui, QtWidgets
from enum import Enum
from tau_ceti_constants import TauCeti
from proxima_centauri_constants import ProximaCentauri
from solar_system_constants import SolarSystem
from HD_219134_constants import HD219134


#
# Simple settings button component
#
class SettingsBtnLayout(QtWidgets.QHBoxLayout):
    def __init__(self, on_click: Callable, btn_width: Optional[int] = None, btn_height: Optional[int] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.addStretch()
        self.btn = QtWidgets.QPushButton()
        if btn_width:
            self.btn.setFixedWidth(btn_width)
        if btn_height:
            self.btn.setFixedHeight(btn_height)
        self.btn.clicked.connect(on_click)
        self.btn.setIcon(QtGui.QIcon('settingsicon.png'))
        self.addWidget(self.btn)


class SettingsKeys(Enum):
    STAR_SYSTEM = "Star system"
    CENTRE_OF_ORBIT = "Centre of orbit"
    OBJECTS_TO_SHOW = "Objects to show"
    ORBIT_TIME = "Orbit time"
    VIEW_TYPE = "View type"
    NUM_ORBITS = "Number of orbits"


class ViewType(Enum):
    TWO_D = "2D"
    THREE_D = "3D"


class StarSystem(Enum):
    SOLAR_SYSTEM = "Solar System"
    TAU_CETI = "Tau Ceti"
    PROXIMA_CENTAURI = "Proxima Centauri"
    HD_219134 = "HD 219134"


DEFAULT_STAR_SYSTEM = StarSystem.SOLAR_SYSTEM

solar_system_enum_to_class: dict = {
    StarSystem.SOLAR_SYSTEM: SolarSystem,
    StarSystem.TAU_CETI: TauCeti,
    StarSystem.PROXIMA_CENTAURI: ProximaCentauri,
    StarSystem.HD_219134: HD219134,
}


#
# Class that has a single static variable SETTINGS.
# Both OrbitPageSettings and OrbitPage have an instance of OrbitSimSettings, and so when OrbitPageSettings manipulates the SETTINGS attribute, that change is also made in the OrbitPage instance
#
class OrbitSimSettings:
    SETTINGS: dict = {
        SettingsKeys.STAR_SYSTEM.value: DEFAULT_STAR_SYSTEM,
        SettingsKeys.CENTRE_OF_ORBIT.value: solar_system_enum_to_class[DEFAULT_STAR_SYSTEM].Planet[solar_system_enum_to_class[DEFAULT_STAR_SYSTEM].SUN].value,
        SettingsKeys.OBJECTS_TO_SHOW.value: [e.value for e in solar_system_enum_to_class[DEFAULT_STAR_SYSTEM].Planet if e.name != "SUN"],
        SettingsKeys.ORBIT_TIME.value: 5,
        SettingsKeys.VIEW_TYPE.value: ViewType.TWO_D.value,
        SettingsKeys.NUM_ORBITS.value: 1,
    }


class CheckBox(QtWidgets.QCheckBox):
    def __init__(self, on_change: Optional[Callable] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.toggled.connect(on_change)


#
# Component that allows the user to choose 2D or 3D in the orbit simulation settings
#
class ViewTypePicker(QtWidgets.QVBoxLayout):
    def __init__(self, settings: OrbitSimSettings, *args, **kwargs):
        margin = kwargs.pop("margin", None)
        alignment = kwargs.pop("alignment", None)
        super().__init__(*args, **kwargs)
        self.settings: OrbitSimSettings = settings
        self.settings_key: str = SettingsKeys.VIEW_TYPE.value
        self.label = QtWidgets.QLabel("View type")
        self.label.setStyleSheet("font-weight: bold;")
        self.addWidget(self.label)
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


#
# Generic component for a horizontal widget that can be used to choose values ranging from integers to an item from a dropdown
#
class HorizontalValuePicker(QtWidgets.QHBoxLayout):
    def __init__(self, value_type: type | str, lbl_text: str, default_val=None, choices: Optional[list] = None,
                 tooltip: Optional[str] = None, on_change: Optional[Callable] = None,
                 fixed_lbl_width: Optional[int] = None, fixed_form_width: Optional[int] = None,
                 fixed_height: Optional[int] = None, padding: Optional[list[int]] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value_type = value_type
        self.label = QtWidgets.QLabel(lbl_text)
        self.label.setStyleSheet("font-weight: bold;")
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
                self.line_edit.setText(str(default_val))
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

    def set_choices(self, choices: list, index: int):
        if self.value_type == "from_multiple":
            self.removeWidget(self.form)
            self.choices = choices
            self.form.clear()
            self.form.addItems(self.choices)
            self.form.setCurrentIndex(index)
            self.addWidget(self.form)


#
# Generic component for a vertical widget that can be used to choose values ranging from integers to an item from a dropdown
#
class VerticalValuePicker(QtWidgets.QVBoxLayout):
    def __init__(self, value_type: type | str, lbl_text: str, default_val=None, choices: Optional[list] = None,
                 tooltip: Optional[str] = None, on_change: Optional[Callable] = None,
                 fixed_lbl_height: Optional[int] = None, fixed_form_height: Optional[int] = None,
                 fixed_width: Optional[int] = None, padding: Optional[list[int]] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value_type = value_type
        self.label = QtWidgets.QLabel(lbl_text)
        self.label.setStyleSheet("font-weight: bold;")
        self.on_change = on_change
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
        elif value_type == "many_from_multiple":
            self.choices = choices
            self.checkboxes = []
            for choice in choices:
                checkbox = CheckBox(lambda: on_change(self.checkboxes),
                                    choice)
                self.addWidget(checkbox)
                self.checkboxes.append(checkbox)
            self.form = self.checkboxes
        else:
            raise TypeError("invalid value type for ValuePicker")
        if fixed_form_height:
            self.form.setFixedHeight(fixed_form_height)
        if fixed_width:
            self.label.setFixedWidth(fixed_width)
            self.form.setFixedWidth(fixed_width)
        if padding:
            self.setContentsMargins(*padding)
        if type(self.form) != list and self.form is not None:
            self.addWidget(self.form)

    def get_value(self):
        if isinstance(self.form, QtWidgets.QComboBox):
            return self.choices[self.form.currentIndex()]
        if isinstance(self.form, QtWidgets.QLineEdit):
            return self.form.text()
        raise TypeError("cannot handle form of type {}".format(type(self.form)))

    def set_choices(self, choices: list, current_index: int = 0, check_all: bool = False):
        if self.value_type == "from_multiple":
            self.choices = []
            self.form.clear()
            self.form.addItems(choices)
            self.choices = choices
            self.form.setCurrentIndex(current_index)
        elif self.value_type == "many_from_multiple":
            while len(self.checkboxes) > len(choices):
                self.removeWidget(self.checkboxes.pop())
            while len(self.checkboxes) < len(choices):
                self.checkboxes.append(CheckBox(
                    lambda: self.on_change(self.checkboxes),
                    ""
                ))
                self.addWidget(self.checkboxes[-1])
            for i, choice in enumerate(choices):
                self.checkboxes[i].setText(choice)
                if check_all:
                    self.checkboxes[i].setChecked(True)

    def set_value(self, new_value):
        if self.value_type in [int, float, str]:
            self.form.setText(str(new_value))
        elif self.value_type == "from_multiple":
            assert new_value in self.choices, "new value must be from choices available in the dropdown"
            self.form.setCurrentIndex(self.choices.index(new_value))
        elif self.value_type == "many_from_multiple":
            for i in range(len(self.form)):
                checkbox: QtWidgets.QCheckBox = self.form[i]
                if checkbox.text() in new_value:
                    self.form[i].setChecked(True)
                else:
                    self.form[i].setChecked(False)


#
# Generic label component for users to view a certain statistic
#
class ValueViewer(QtWidgets.QVBoxLayout):
    def __init__(self, k: str, v: str = "-", fixed_key_height: Optional[int] = None,
                 fixed_value_height: Optional[int] = None, fixed_width: Optional[int] = None,
                 alignment: Optional[QtCore.Qt.AlignmentFlag] = None, padding: Optional[list[int]] = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.key_label = QtWidgets.QLabel(k)
        self.key_label.setWordWrap(True)
        self.addWidget(self.key_label)
        if fixed_key_height:
            self.key_label.setFixedHeight(fixed_key_height)
        self.key_label.setStyleSheet("font-weight: bold;")
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
        self.label.setText(str(new_text) if new_text else "-")
