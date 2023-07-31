from enum import Enum
#
# Using Decimal as the data type for all numerical calculations to
# eliminate floating-point inaccuracies
#
from decimal import Decimal

earth_mass: Decimal = Decimal(5.9742) * Decimal(10) ** Decimal(24)


#
# Measured in kg
#
class Masses(Enum):
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
class Eccentricities(Enum):
    SUN = 0
    MERCURY = 0.21
    VENUS = 0.01
    EARTH = 0.02
    MARS = 0.09
    JUPITER = 0.05
    SATURN = 0.06
    URANUS = 0.05
    NEPTUNE = 0.01
    PLUTO = 0.25


#
# Measured in A.U.
#
class SemiMajorAxes(Enum):
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
class SemiMinorAxes(Enum):
    SUN = SemiMajorAxes.SUN.value * (Decimal(1) - Eccentricities.SUN.value ** 2)
    MERCURY = SemiMajorAxes.MERCURY.value * (Decimal(1) - Eccentricities.MERCURY.value ** 2)
    VENUS = SemiMajorAxes.VENUS.value * (Decimal(1) - Eccentricities.VENUS.value ** 2)
    EARTH = SemiMajorAxes.EARTH.value * (Decimal(1) - Eccentricities.EARTH.value ** 2)
    MARS = SemiMajorAxes.MARS.value * (Decimal(1) - Eccentricities.MARS.value ** 2)
    JUPITER = SemiMajorAxes.JUPITER.value * (Decimal(1) - Eccentricities.JUPITER.value ** 2)
    SATURN = SemiMajorAxes.SATURN.value * (Decimal(1) - Eccentricities.SATURN.value ** 2)
    URANUS = SemiMajorAxes.URANUS.value * (Decimal(1) - Eccentricities.URANUS.value ** 2)
    NEPTUNE = SemiMajorAxes.NEPTUNE.value * (Decimal(1) - Eccentricities.NEPTUNE.value ** 2)
    PLUTO = SemiMajorAxes.PLUTO.value * (Decimal(1) - Eccentricities.PLUTO.value ** 2)


#
# Measured in years
#
class OrbitalPeriods(Enum):
    SUN = Decimal(0)
    MERCURY

class GlobalConstants(Enum):
    FRAME_RATE = 60
    G_CONSTANT = Decimal(6.67) * Decimal(10) ** Decimal(-11)
