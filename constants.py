from solar_system_constants import SolarSystem
from tau_ceti_constants import TauCeti
from HD_219134_constants import HD219134
from proxima_centauri_constants import ProximaCentauri
from enum import Enum

class Constants:
    SOLAR_SYSTEM = SolarSystem
    TAU_CETI = TauCeti
    HD_219134 = HD219134
    PROXIMA_CENTAURI = ProximaCentauri

    class Names(Enum):
        SOLAR_SYSTEM = "Solar System"
        TAU_CETI = "Tau Ceti System"
        HD_219134 = "HD 219134 System"
        PROXIMA_CENTAURI = "Proxima Centauri System"
