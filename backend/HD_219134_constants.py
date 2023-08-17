from enum import Enum
#
# Using Decimal as the data type for all numerical calculations to
# eliminate floating-point inaccuracies
#
from decimal import Decimal


class HD219134:
    SUN = "HD_219134"

    class Planet(Enum):
        HD_219134 = "HD 219314"
        b = "HD 219314 b"
        c = "HD 219314 c"
        f = "HD 219314 f"
        d = "HD 219314 d"
        g = "HD 219314 g"
        h = "HD 219314 h"

    class Mass(Enum):
        HD_219134 = Decimal('0.75') * Decimal('333030')
        b = Decimal('4.74')
        c = Decimal('4.36')
        d = Decimal('16.170')
        f = Decimal('7.3')
        g = Decimal('10.80622')
        h = Decimal('0.34') * Decimal('317.907')

    class Eccentricity(Enum):
        HD_219134 = Decimal('0')
        b = Decimal('0')
        c = Decimal('0.062')
        f = Decimal('0.148')
        d = Decimal('0.138')
        g = Decimal('0')
        h = Decimal('0.06')

    class SemiMajorAxis(Enum):
        HD_219134 = Decimal('0')
        b = Decimal('0.03876')
        c = Decimal('0.06530')
        f = Decimal('0.1463')
        d = Decimal('0.2370')
        g = Decimal('0.3753')
        h = Decimal('3.11')

    class SemiMinorAxis(Enum):
        HD_219134 = Decimal('0')
        b = Decimal('0.03876')
        c = Decimal('0.06504899')
        f = Decimal('0.143095')
        d = Decimal('0.232487')
        g = Decimal('0.3753')
        h = Decimal('3.09880')

    class OrbitalPeriod(Enum):
        HD_219134 = Decimal('0')
        b = Decimal('3.092926') / Decimal('365')
        c = Decimal('6.76458') / Decimal('365')
        f = Decimal('22.717') / Decimal('365')
        d = Decimal('46.859') / Decimal('365')
        g = Decimal('94.2') / Decimal('365')
        h = Decimal('2100.6') / Decimal('365')

    class InclinationAngle(Enum):
        HD_219134 = Decimal('0')
        b = Decimal('1.4844')
        c = Decimal('1.5233')
        f = Decimal('0')
        d = Decimal('0')
        g = Decimal('0')
        h = Decimal('0')
