import numpy as np
from constants import Constants

class CalcFunctions:
    @staticmethod
    def orbital_vals_2d(theta_vals, planet: str, solar_system: str):
        b = float(Constants.__dict__[solar_system].SemiMinorAxis[planet].value)
        e = float(Constants.__dict__[solar_system].Eccentricity[planet].value)
        r = b / (1 - e * np.cos(theta_vals))
        x = r * np.cos(theta_vals)
        y = r * np.sin(theta_vals)
        return (x, y)

    @staticmethod
    def orbital_vals_3d(theta_vals, planet: str, solar_system: str):
        b = float(Constants.__dict__[solar_system].SemiMinorAxis[planet].value)
        e = float(Constants.__dict__[solar_system].Eccentricity[planet].value)
        angle = float(Constants.__dict__[solar_system].InclinationAngle[planet].value)
        r = b / (1 - e * np.cos(theta_vals))
        x = r * np.cos(theta_vals) * np.cos(angle)
        y = r * np.sin(theta_vals)
        z = r * np.cos(theta_vals) * np.sin(angle)
        return (x, y, z)