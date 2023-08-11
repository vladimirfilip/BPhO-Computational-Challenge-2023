from enum import Enum
#
# Using Decimal as the data type for all numerical calculations to
# eliminate floating-point inaccuracies
#
from decimal import Decimal

class Planet(Enum):
    PROXIMA_CENTAURI: "Proxima Centauri"
    d: "Proxima Centauri d"
    b: "Proxima Centauri b"

class Eccentricity(Enum):
    PROXIMA_CENTAURI: Decimal(0)
    d: Decimal(0.04)
    b: Decimal(0.109)

class SemiMajorAxis(Enum):
    PROXIMA_CENTAURI: Decimal(0)
    d: Decimal(0.02885)
    b: Decimal

class SemiMinorAxis(Enum):
    d: SemiMajorAxis.d.value * (Decimal(1) - Eccentricity.d.value ** 2)
    b: SemiMajorAxis.b.value * (Decimal(1) - Eccentricity.b.value ** 2)

class OrbitalPeriod(Enum):
    d: Decimal(5.122)
    b: Decimal(11.18418)

class InclinationAngle(Enum):
    d: Decimal(0)
    b: Decimal(0)