from typing import Callable, Optional

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from backend.constants import Constants
import numpy as np
import math
from backend.calc_functions import CalcFunctions
from random import sample

matplotlib.use('TkAgg')


class SpiroAnimation:
    COLOURS = ["black", "red", "orange", "green", "blue", "darkviolet"]
    LINES_PER_ORBIT: int = 70

    def __init__(self, fig, solar_system: str, planet_1: str, planet_2: str, N: int, speed: str, post_draw_callback: Optional[Callable] = None):
        self._solar_system = solar_system
        self.post_draw_callback = post_draw_callback
        self._constants = Constants.__dict__[self._solar_system]

        self._planet_1 = planet_1
        self._planet_2 = planet_2

        # Total number of orbits of outermost planet
        self._num_orbits = N

        # Total number of lines to show
        self._num_lines = N * SpiroAnimation.LINES_PER_ORBIT

        # Endpoints of lines between planets
        self._spiro_data = []

        self._lines = []

        self._colour_1, self._colour_2 = sample(SpiroAnimation.COLOURS, 2)

        # Difference in time between drawing of two consecutive lines
        match speed:
            case "slow": self._time_diff = 100
            case "medium": self._time_diff = 40
            case "fast": self._time_diff = 10

        self._fig: plt.Figure = fig
        self._ax = self._fig.subplots()
        self._ax.set_title(f"Spirograph with {self._planet_1} and {self._planet_2}",
                           fontsize=10)
        self._ax.get_xaxis().set_visible(False)
        self._ax.get_yaxis().set_visible(False)
        self._ax.spines['top'].set_visible(False)
        self._ax.spines['right'].set_visible(False)
        self._ax.spines['left'].set_visible(False)
        self._ax.spines['bottom'].set_visible(False)
        self._ax.grid(False)

        self._orbit_1 = None
        self._anim_data_1 = []
        self._anim_1 = self._ax.plot([], [], marker="o", color=self._colour_1)[0]
        self._orbit_2 = None
        self._anim_data_2 = []
        self._anim_2 = self._ax.plot([], [], marker="o", color=self._colour_2)[0]

        self.generate_line_data()
        self.set_limits()
        self.calculate_orbit_data()
        self.calculate_anim_data()
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

    def set_limits(self):
        min_x = min([min(vals[0]) for vals in self._spiro_data])
        max_x = max([max(vals[0]) for vals in self._spiro_data])
        min_y = min([min(vals[1]) for vals in self._spiro_data])
        max_y = max([max(vals[1]) for vals in self._spiro_data])
        padding_x = (max_x - min_x) / 20
        padding_y = (max_y - min_y) / 20
        self._ax.set_xlim([min_x - padding_x, max_x + padding_x])
        self._ax.set_ylim([min_y - padding_y, max_y + padding_y])

    def calculate_orbit_data(self):
        theta_vals = np.linspace(0, math.pi * 2, 1000)
        x_1, y_1 = CalcFunctions.orbital_vals_2d(theta_vals, self._planet_1, self._solar_system)
        x_2, y_2 = CalcFunctions.orbital_vals_2d(theta_vals, self._planet_2, self._solar_system)
        self._orbit_1 = self._ax.plot(x_1, y_1, color=self._colour_1, lw=2,
                                      label=self._constants.Planet[self._planet_1].value)[0]
        self._orbit_2 = self._ax.plot(x_2, y_2, color=self._colour_2, lw=2,
                                      label=self._constants.Planet[self._planet_2].value)[0]

    def calculate_anim_data(self):
        period_1 = float(self._constants.OrbitalPeriod[self._planet_1].value)
        period_2 = float(self._constants.OrbitalPeriod[self._planet_2].value)
        max_period = max(period_1, period_2)
        time_vals = np.linspace(0, max_period * self._num_orbits, self._num_lines)
        theta_vals_1 = (2 * math.pi * time_vals) / period_1
        theta_vals_2 = (2 * math.pi * time_vals) / period_2
        self._anim_data_1 = CalcFunctions.orbital_vals_2d(theta_vals_1, self._planet_1, self._solar_system)
        self._anim_data_2 = CalcFunctions.orbital_vals_2d(theta_vals_2, self._planet_2, self._solar_system)

    def init_func(self):
        self._lines = [self._ax.plot([], [], lw=0.15, color="black")[0] for _ in range(self._num_lines)]
        return self._lines + [self._anim_1, self._anim_2, self._orbit_1, self._orbit_2]

    def animate(self, i):
        self._anim_1.set_data([self._anim_data_1[0][i]], [self._anim_data_1[1][i]])
        self._anim_2.set_data([self._anim_data_2[0][i]], [self._anim_data_2[1][i]])
        self._lines[i].set_data(self._spiro_data[i][0], self._spiro_data[i][1])
        if self.post_draw_callback:
            self.post_draw_callback(i // SpiroAnimation.LINES_PER_ORBIT, i)
        return self._lines + [self._anim_1, self._anim_2, self._orbit_1, self._orbit_2]

    def create_animation(self):
        self._ax.legend(loc="upper right")
        self.ani = FuncAnimation(self._fig, self.animate, frames=self._num_lines, interval=self._time_diff, repeat=True, blit=True, init_func=self.init_func)

if __name__ == "__main__":
    SpiroAnimation("TAU_CETI", "g", "h", 8, 700, 0.5)