import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from constants import Constants
import numpy as np
import math
from calc_functions import CalcFunctions

matplotlib.use('TkAgg')


class SpiroAnimation:
    def __init__(self, fig, solar_system: str, planet_1: str, planet_2: str, N: int, d, time_diff: float):
        self._solar_system = solar_system
        self._constants = Constants.__dict__[self._solar_system]

        self._planet_1 = planet_1
        self._planet_2 = planet_2

        # Total number of orbits of outermost planet
        self._num_orbits = N

        # Total number of lines to show
        self._num_lines = d

        # Endpoints of lines between planets
        self._spiro_data = []

        self._lines = []

        # Difference in time between drawing of two consecutive lines
        self._time_diff = time_diff

        self._fig: plt.Figure = fig
        self._ax = self._fig.subplots()
        self._ax.set_xlim([-1, 1])
        self._ax.set_ylim([-1, 1])

        self.generate_line_data()
        self.create_animation()

    def calculate_point(self, t, e, b, P):
        theta = (2 * math.pi * t) / P
        r = b / (1 - e * np.cos(float(theta)))
        return [r * np.cos(float(theta)), r * np.sin(float(theta))]

    def generate_line_data(self):
        period_1 = float(self._constants.OrbitalPeriod[self._planet_1].value)
        period_2 = float(self._constants.OrbitalPeriod[self._planet_2].value)
        max_period = max(period_1, period_2)

        # Regular points in time for each line drawn between the planets
        time_vals = np.linspace(0, self._num_orbits * float(max_period), self._num_lines)
        eccentricity_1 = float(self._constants.Eccentricity[self._planet_1].value)
        eccentricity_2 = float(self._constants.Eccentricity[self._planet_2].value)
        semi_minor_1 = float(self._constants.SemiMinorAxis[self._planet_1].value)
        semi_minor_2 = float(self._constants.SemiMinorAxis[self._planet_2].value)

        for time in time_vals:
            x_1, y_1 = self.calculate_point(time, eccentricity_1, semi_minor_1, period_1)
            x_2, y_2 = self.calculate_point(time, eccentricity_2, semi_minor_2, period_2)
            self._spiro_data.append(([x_1, x_2], [y_1, y_2]))

    def init_func(self):
        self._lines = [self._ax.plot([], [], lw=0.2, color="black")[0] for _ in range(self._num_lines)]
        return self._lines

    def animate(self, i):
        self._lines[i].set_data(self._spiro_data[i][0], self._spiro_data[i][1])
        return self._lines
        #self._ax.plot(self._spiro_data[i][0], self._spiro_data[i][1], linewidth='0.5', color='black')

    def create_animation(self):
        self.ani = FuncAnimation(self._fig, self.animate, frames=self._num_lines, interval=self._time_diff, repeat=True, blit=True, init_func=self.init_func)

if __name__ == "__main__":
    SpiroAnimation("TAU_CETI", "g", "h", 8, 700, 0.5)