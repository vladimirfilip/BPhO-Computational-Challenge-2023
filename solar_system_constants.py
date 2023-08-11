from enum import Enum
#
# Using Decimal as the data type for all numerical calculations to
# eliminate floating-point inaccuracies
#
from decimal import Decimal

earth_mass: Decimal = Decimal(5.9742) * Decimal(10) ** Decimal(24)


class Planet(Enum):
    SUN = "Sun"
    MERCURY = "Mercury"
    VENUS = "Venus"
    EARTH = "Earth"
    MARS = "Mars"
    JUPITER = "Jupiter"
    SATURN = "Saturn"
    URANUS = "Uranus"
    NEPTUNE = "Neptune"
    PLUTO = "PLUTO"


#
# Measured in kg
#
class Mass(Enum):
    SUN = Decimal(332837) * earth_mass
    MERCURY = Decimal(0.055) * earth_mass
    VENUS = Decimal(0.815) * earth_mass
    EARTH = earth_mass
    MARS = Decimal(0.107) * earth_mass
    JUPITER = Decimal(317.85) * earth_mass
    SATURN = Decimal(95.159) * earth_mass
    URANUS = Decimal(14.5) * earth_mass
    NEPTUNE = Decimal(17.204) * earth_mass
    PLUTO = Decimal(0.003) * earth_mass


#
# Scalar
#
class Eccentricity(Enum):
    SUN = Decimal(0)
    MERCURY = Decimal(0.21)
    VENUS = Decimal(0.01)
    EARTH = Decimal(0.02)
    MARS = Decimal(0.09)
    JUPITER = Decimal(0.05)
    SATURN = Decimal(0.06)
    URANUS = Decimal(0.05)
    NEPTUNE = Decimal(0.01)
    PLUTO = Decimal(0.25)


#
# Measured in A.U.
#
class SemiMajorAxis(Enum):
    SUN = Decimal(0)
    MERCURY = Decimal(0.387)
    VENUS = Decimal(0.723)
    EARTH = Decimal(1)
    MARS = Decimal(1.523)
    JUPITER = Decimal(5.202)
    SATURN = Decimal(9.576)
    URANUS = Decimal(19.293)
    NEPTUNE = Decimal(30.246)
    PLUTO = Decimal(39.509)


#
# b = a(1 - eccentricity^2)
#
class SemiMinorAxis(Enum):
    SUN = SemiMajorAxis.SUN.value * (Decimal(1) - Eccentricity.SUN.value ** 2)
    MERCURY = SemiMajorAxis.MERCURY.value * (Decimal(1) - Eccentricity.MERCURY.value ** 2)
    VENUS = SemiMajorAxis.VENUS.value * (Decimal(1) - Eccentricity.VENUS.value ** 2)
    EARTH = SemiMajorAxis.EARTH.value * (Decimal(1) - Eccentricity.EARTH.value ** 2)
    MARS = SemiMajorAxis.MARS.value * (Decimal(1) - Eccentricity.MARS.value ** 2)
    JUPITER = SemiMajorAxis.JUPITER.value * (Decimal(1) - Eccentricity.JUPITER.value ** 2)
    SATURN = SemiMajorAxis.SATURN.value * (Decimal(1) - Eccentricity.SATURN.value ** 2)
    URANUS = SemiMajorAxis.URANUS.value * (Decimal(1) - Eccentricity.URANUS.value ** 2)
    NEPTUNE = SemiMajorAxis.NEPTUNE.value * (Decimal(1) - Eccentricity.NEPTUNE.value ** 2)
    PLUTO = SemiMajorAxis.PLUTO.value * (Decimal(1) - Eccentricity.PLUTO.value ** 2)


#
# Measured in years
#
class OrbitalPeriod(Enum):
    SUN = Decimal(0)
    MERCURY = Decimal(0.241)
    VENUS = Decimal(0.615)
    EARTH = Decimal(1)
    MARS = Decimal(1.881)
    JUPITER = Decimal(11.861)
    SATURN = Decimal(29.628)
    URANUS = Decimal(84.747)
    NEPTUNE = Decimal(166.344)
    PLUTO = Decimal(248.348)


class InclinationAngle(Enum):
    MERCURY = Decimal(7)
    VENUS = Decimal(3.39)
    EARTH = Decimal(0)
    MARS = Decimal(1.85)
    JUPITER = Decimal(1.31)
    SATURN = Decimal(2.49)
    URANUS = Decimal(0.77)
    NEPTUNE = Decimal(1.77)
    PLUTO = Decimal(17.5)


class GlobalConstants(Enum):
    FRAME_RATE = 47
    FRAME_INTERVAL = 40
    G_CONSTANT = Decimal(6.67) * Decimal(10) ** Decimal(-11)
