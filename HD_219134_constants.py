from enum import Enum
#
# Using Decimal as the data type for all numerical calculations to
# eliminate floating-point inaccuracies
#
from decimal import Decimal

class Planets(Enum):
    HD_219134: "HD 219314"
    b: "HD 219314 b"
    c: "HD 219314 c"
    f: "HD 219314 f"
    d: "HD 219314 d"
    g: "HD 219314 g"
    h: "HD 219314 h"

class Eccentricity(Enum):
    b: Decimal(0)
    c: Decimal(0.062)
    f: Decimal(0.148)
    d: Decimal(0.138)
    g: Decimal(0)
    h: Decimal(0.06)

class SemiMajorAxis(Enum):
    b: Decimal(0.03876)
    c: Decimal(0.06530)
    f: Decimal(0.1463)
    d: Decimal(0.2370)
    g: Decimal(0.3753)
    h: Decimal(3.11)

class SemiMinorAxis(Enum):
    b: SemiMajorAxis.b.value * (Decimal(1) - Eccentricity.b.value ** 2)
    c: SemiMajorAxis.c.value * (Decimal(1) - Eccentricity.c.value ** 2)
    f: SemiMajorAxis.f.value * (Decimal(1) - Eccentricity.f.value ** 2)
    d: SemiMajorAxis.d.value * (Decimal(1) - Eccentricity.d.value ** 2)
    g: SemiMajorAxis.g.value * (Decimal(1) - Eccentricity.g.value ** 2)
    h: SemiMajorAxis.h.value * (Decimal(1) - Eccentricity.h.value ** 2)

class OrbitalPeriod(Enum):
    b: Decimal(3.092926)
    c: Decimal(6.76458)
    f: Decimal(22.717)
    d: Decimal(46.859)
    g: Decimal(94.2)
    h: Decimal(2100.6)

class InclinationAngle(Enum):
    b: Decimal(85.05)
    c: Decimal(87.28)
    f: Decimal(0)
    d: Decimal(0)
    g: Decimal(0)
    h: Decimal(0)