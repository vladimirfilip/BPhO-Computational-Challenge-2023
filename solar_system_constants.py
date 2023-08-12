from enum import Enum
#
# Using Decimal as the data type for all numerical calculations to
# eliminate floating-point inaccuracies
#
from decimal import Decimal

earth_mass: Decimal = Decimal(5.9742) * Decimal(10) ** Decimal(24)


class SolarSystem:
    SUN = "SUN"
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
        SUN = Decimal('332837')
        MERCURY = Decimal('0.055')
        VENUS = Decimal('0.815')
        EARTH = Decimal('1')
        MARS = Decimal('0.107')
        JUPITER = Decimal('317.85')
        SATURN = Decimal('95.159')
        URANUS = Decimal('14.5')
        NEPTUNE = Decimal('17.204')
        PLUTO = Decimal('0.003')

    #
    # Scalar
    #
    class Eccentricity(Enum):
        SUN = Decimal('0')
        MERCURY = Decimal('0.21')
        VENUS = Decimal('0.01')
        EARTH = Decimal('0.02')
        MARS = Decimal('0.09')
        JUPITER = Decimal('0.05')
        SATURN = Decimal('0.06')
        URANUS = Decimal('0.05')
        NEPTUNE = Decimal('0.01')
        PLUTO = Decimal('0.25')

    #
    # Measured in A.U.
    #
    class SemiMajorAxis(Enum):
        SUN = Decimal('0')
        MERCURY = Decimal('0.387')
        VENUS = Decimal('0.723')
        EARTH = Decimal('1')
        MARS = Decimal('1.523')
        JUPITER = Decimal('5.202')
        SATURN = Decimal('9.576')
        URANUS = Decimal('19.293')
        NEPTUNE = Decimal('30.246')
        PLUTO = Decimal('39.509')

    #
    # b = a(1 - eccentricity^2)
    #
    class SemiMinorAxis(Enum):
        SUN = Decimal('0')
        MERCURY = Decimal('0.36993')
        VENUS = Decimal('0.72293')
        EARTH = Decimal('0.9996')
        MARS = Decimal('1.51066')
        JUPITER = Decimal('5.18900')
        SATURN = Decimal('9.54153')
        URANUS = Decimal('19.24477')
        NEPTUNE = Decimal('30.24298')
        PLUTO = Decimal('37.03969')

    #
    # Measured in years
    #
    class OrbitalPeriod(Enum):
        SUN = Decimal('0')
        MERCURY = Decimal('0.241')
        VENUS = Decimal('0.615')
        EARTH = Decimal('1')
        MARS = Decimal('1.881')
        JUPITER = Decimal('11.861')
        SATURN = Decimal('29.628')
        URANUS = Decimal('84.747')
        NEPTUNE = Decimal('166.344')
        PLUTO = Decimal('248.348')

    class InclinationAngle(Enum):
        MERCURY = Decimal('0.1222')
        VENUS = Decimal('0.05917')
        EARTH = Decimal('0')
        MARS = Decimal('0.03229')
        JUPITER = Decimal('0.02286')
        SATURN = Decimal('0.04346')
        URANUS = Decimal('0.01344')
        NEPTUNE = Decimal('0.03089')
        PLUTO = Decimal('0.3054')

    class GlobalConstants(Enum):
        FRAME_RATE = 47
        FRAME_INTERVAL = 40
        G_CONSTANT = Decimal('6.67') * Decimal('10') ** Decimal('-11')
