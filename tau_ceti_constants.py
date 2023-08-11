from enum import Enum
#
# Using Decimal as the data type for all numerical calculations to
# eliminate floating-point inaccuracies
#
from decimal import Decimal

class Planet(Enum):
    TAU_CETI: "Tau Ceti"
    g: "Tau Ceti g"
    h: "Tau Ceti h"
    e: "Tau Ceti e"
    f: "Tau Ceti f"

class Eccentricity(Enum):
    TAU_CETI: 0
    g: Decimal(0.06)
    h: Decimal(0.23)
    e: Decimal(0.18)
    f: Decimal(0.16)

class SemiMajorAxis(Enum):
    TAU_CETI: Decimal(0)
    g: Decimal(0.133)
    h: Decimal(0.243)
    e: Decimal(0.538)
    f: Decimal(1.334)

class SemiMinorAxis(Enum):
    TAU_CETI: Decimal(0)
    g: SemiMajorAxis.g.value * (Decimal(1) - Eccentricity.g.value ** 2)
    h: SemiMajorAxis.h.value * (Decimal(1) - Eccentricity.h.value ** 2)
    e: SemiMajorAxis.e.value * (Decimal(1) - Eccentricity.e.value ** 2)
    f: SemiMajorAxis.f.value * (Decimal(1) - Eccentricity.f.value ** 2)

class OrbitalPeriod(Enum):
    TAU_CETI: Decimal(0)
    g: Decimal(20)
    h: Decimal(49.41)
    e: Decimal(162.87)
    f: Decimal(636.13)

class InclinationAngle(Enum):
    g: 0
    h: 0
    e: 0
    f: 0

