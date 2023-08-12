from enum import Enum
#
# Using Decimal as the data type for all numerical calculations to
# eliminate floating-point inaccuracies
#
from decimal import Decimal


class ProximaCentauri:
    SUN = "PROXIMA_CENTAURI"

    class Planet(Enum):
        PROXIMA_CENTAURI = "Proxima Centauri"
        d = "Proxima Centauri d"
        b = "Proxima Centauri b"

    class Mass(Enum):
        PROXIMA_CENTAURI = Decimal('0.1221') * Decimal('333030')
        d = Decimal('0.26')
        b = Decimal('1.07')

    class Eccentricity(Enum):
        PROXIMA_CENTAURI = Decimal('0')
        d = Decimal('0.04')
        b = Decimal('0.109')

    class SemiMajorAxis(Enum):
        PROXIMA_CENTAURI = Decimal('0')
        d = Decimal('0.02885')
        b = Decimal('0.04857')

    class SemiMinorAxis(Enum):
        d = Decimal('0.0288038')
        b = Decimal('0.0479930')

    class OrbitalPeriod(Enum):
        d = Decimal('5.122') / Decimal('365')
        b = Decimal('11.18418') / Decimal('365')

    class InclinationAngle(Enum):
        d = Decimal('0')
        b = Decimal('0')
