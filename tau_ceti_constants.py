from enum import Enum
#
# Using Decimal as the data type for all numerical calculations to
# eliminate floating-point inaccuracies
#
from decimal import Decimal

class TauCeti:
    SUN = "TAU_CETI"
    class Planet(Enum):
        TAU_CETI = "Tau Ceti"
        g = "Tau Ceti g"
        h = "Tau Ceti h"
        e = "Tau Ceti e"
        f = "Tau Ceti f"

    class Eccentricity(Enum):
        TAU_CETI = Decimal('0')
        g = Decimal('0.06')
        h = Decimal('0.23')
        e = Decimal('0.18')
        f = Decimal('0.16')

    class SemiMajorAxis(Enum):
        TAU_CETI = Decimal('0')
        g = Decimal('0.133')
        h = Decimal('0.243')
        e = Decimal('0.538')
        f = Decimal('1.334')

    class SemiMinorAxis(Enum):
        TAU_CETI = Decimal('0')
        g = Decimal('0.132521')
        h = Decimal('0.230145')
        e = Decimal('0.520569')
        f = Decimal('1.299850')

    class OrbitalPeriod(Enum):
        TAU_CETI = Decimal('0')
        g = Decimal('20') / Decimal('365')
        h = Decimal('49.41') / Decimal('365')
        e = Decimal('162.87') / Decimal('365')
        f = Decimal('636.13') / Decimal('365')

    class InclinationAngle(Enum):
        g = Decimal('0')
        h = Decimal('0')
        e = Decimal('0')
        f = Decimal('0')