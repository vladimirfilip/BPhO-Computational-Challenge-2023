from typing import Optional, Callable

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from constants import Constants
import numpy as np
import math
from calc_functions import CalcFunctions
from random import shuffle

matplotlib.use('TkAgg')


class Animation3D:
    FRAME_DURATION = 20
    COLOURS = ["black", "orange", "green", "blue", "darkviolet", "cyan", "lime", "pink", "indigo"]

    def __init__(self, fig, solar_system: str, planets: list[str], centre: str, orbit_duration: float, num_orbits: int,
                 post_draw_callback: Optional[Callable] = None):
        self.post_draw_callback = post_draw_callback
        self._solar_system = solar_system
        self.constants = Constants.__dict__[self._solar_system]

        # Planets to show in animation
        self._planets = planets

        # Total number of orbits of outermost planet
        self._num_orbits = num_orbits

        # Total number of frames for one orbit of outermost planet
        self._num_frames = None

        # Line objects for orbital paths
        self._lines = []

        # Point objects for planet position
        self._anims = []

        # Line data for orbital paths
        self._line_data = {}

        # Point data for obital path
        self._anim_data = {}

        # Orbital angle values
        self._theta_vals = {planet: [] for planet in self._planets}

        # Name of planet at centre of animation
        self._centre = centre

        self._centre_line_vals = (0, 0, 0)
        self._centre_anim_vals = (0, 0, 0)

        # Duration of outermost orbit in seconds
        self._orbit_duration = orbit_duration

        self.colours = Animation3D.COLOURS.copy()
        shuffle(self.colours)

        self._fig: plt.Figure = fig
        self._ax = self._fig.add_subplot(111, projection="3d")
        self._ax.set_title(f"Animated 3D orbits of planets in the {Constants.Names[self._solar_system].value}, "
                           f"centre {self.constants.Planet[self._centre].value}",
                           y=0.97,
                           fontsize=10)
        self._fig.tight_layout()
        self._ax.set_xlabel("x / AU")
        self._ax.set_ylabel("y / AU")
        self._ax.set_zlabel("z / AU")

        self.calculate_line_vals()
        self.set_limits()
        self.calculate_anim_vals()
        self.create_animation()

    def calculate_line_vals(self):
        periods = [float(self.constants.OrbitalPeriod[planet].value) for planet in self._planets]
        time_vals = np.linspace(0, float(max(periods) * self._num_orbits), 1000)
        # Generates points for orbital path of every planet at regular intervals in orbital angle
        if self._centre != self.constants.SUN:
            theta = (2 * math.pi * time_vals) / float(self.constants.OrbitalPeriod[self._centre].value)
            self._centre_line_vals = CalcFunctions.orbital_vals_3d(theta_vals=theta,
                                                                   planet=self._centre,
                                                                   solar_system=self._solar_system)

        for planet in self._planets:
            theta = (2 * math.pi * time_vals) / float(self.constants.OrbitalPeriod[planet].value)
            x_vals, y_vals, z_vals = CalcFunctions.orbital_vals_3d(theta_vals=theta,
                                                                   planet=planet,
                                                                   solar_system=self._solar_system)
            # Subtracts coordinates of reference planet at each corresponding orbital angle
            self._line_data[planet] = (x_vals - self._centre_line_vals[0],
                                       y_vals - self._centre_line_vals[1],
                                       z_vals - self._centre_line_vals[2])

    def calculate_anim_vals(self):
        periods = [self.constants.OrbitalPeriod[planet].value for planet in self._planets]
        max_period = float(max(periods))

        # Calculates total number of frames that will make up animation
        self._num_frames = round((self._orbit_duration * 1000 * self._num_orbits) / Animation3D.FRAME_DURATION)
        time_vals = np.linspace(0, max_period * self._num_orbits, self._num_frames)

        if self._centre != self.constants.SUN:
            # Calculates orbital angles at corresponding poins in time
            theta_vals = (2 * math.pi * time_vals) / float(self.constants.OrbitalPeriod[self._centre].value)
            self._centre_anim_vals = CalcFunctions.orbital_vals_3d(theta_vals=theta_vals,
                                                                   planet=self._centre,
                                                                   solar_system=self._solar_system)

        for planet in self._planets:
            theta_vals = (2 * math.pi * time_vals) / float(self.constants.OrbitalPeriod[planet].value)
            self._theta_vals[planet] += list(theta_vals)
            x_vals, y_vals, z_vals = CalcFunctions.orbital_vals_3d(theta_vals=theta_vals,
                                                                   planet=planet,
                                                                   solar_system=self._solar_system)
            self._anim_data[planet] = (x_vals - self._centre_anim_vals[0],
                                       y_vals - self._centre_anim_vals[1],
                                       z_vals - self._centre_anim_vals[2])

    def set_limits(self):
        min_x = min([min(vals[0]) for vals in self._line_data.values()])
        max_x = max([max(vals[0]) for vals in self._line_data.values()])
        min_y = min([min(vals[1]) for vals in self._line_data.values()])
        max_y = max([max(vals[1]) for vals in self._line_data.values()])
        min_z = min([min(vals[2]) for vals in self._line_data.values()])
        max_z = max([max(vals[2]) for vals in self._line_data.values()])
        padding_x = (max_x - min_x) / 20
        padding_y = (max_y - min_y) / 20
        padding_z = (max_z - min_z) / 2
        self._ax.set_xlim([min_x - padding_x, max_x + padding_x])
        self._ax.set_ylim([min_y - padding_y, max_y + padding_y])
        if padding_z == 0:
            self._ax.set_zlim([min_z - 0.04, max_z + 0.04])
        else:
            self._ax.set_zlim([min_z - padding_z, max_z + padding_z])

    def init_func(self):
        for line in self._anims:
            line.set_xdata([])
            line.set_ydata([])
            line.set_3d_properties([])
        return self._lines + self._anims

    def animate(self, i):
        coords = []
        for j, current_planet in enumerate(self._planets):
            current_x = self._anim_data[current_planet][0][i]
            current_y = self._anim_data[current_planet][1][i]
            current_z = self._anim_data[current_planet][2][i]
            coords.append([current_x, current_y, current_z])
            self._anims[j].set_xdata([current_x])
            self._anims[j].set_ydata([current_y])
            self._anims[j].set_3d_properties([current_z])
        if self.post_draw_callback:
            self.post_draw_callback([self._theta_vals[planet][i] for planet in self._planets], coords)
        return self._lines + self._anims

    def create_animation(self):
        self._ax.set_box_aspect((3, 3, 1))
        self._ax.view_init(-335.38, 79.14)

        if self._centre == self.constants.SUN:
            self._lines.append(self._ax.plot([0], [0], [0], color="yellow", marker="o", lw=2, markersize=10,
                                             label=self._centre)[0])
        else:
            self._lines.append(self._ax.plot([0], [0], [0], color="red", marker="o", lw=2, markersize=10,
                                             label=self._centre)[0])

        # Initialises line objects for orbital paths and points
        for i in range(len(self._planets)):
            planet = self._planets[i]
            self._anims.append(self._ax.plot([], [], [], color=self.colours[i], marker="o")[0])
            self._lines.append(self._ax.plot(self._line_data[planet][0],
                                             self._line_data[planet][1],
                                             self._line_data[planet][2],
                                             color=self.colours[i],
                                             label=planet,
                                             lw=2)[0])
        self._ax.legend(bbox_to_anchor=(1.2, 0.9))

        self.ani = FuncAnimation(self._fig,
                                 self.animate,
                                 frames=self._num_frames,
                                 interval=Animation3D.FRAME_DURATION,
                                 repeat=True,
                                 blit=True,
                                 init_func=self.init_func)
        # ani.save("3d_animation.gif", fps=25)


if __name__ == "__main__":
    Animation3D("HD_219134", ["b", "c"], "HD_219134", 3)
