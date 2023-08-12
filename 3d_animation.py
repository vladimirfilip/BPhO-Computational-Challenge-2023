import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from constants import Constants
import numpy as np
import math
from calc_functions import CalcFunctions

matplotlib.use('TkAgg')


class Animation3D:
    FRAME_DURATION = 20

    def __init__(self, solar_system: str, planets: list[str], centre: str, orbit_duration: float):
        self._solar_system = solar_system
        self.constants = Constants.__dict__[self._solar_system]

        # Planets to show in animation
        self._planets = planets

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

        # Name of planet at centre of animation
        self._centre = centre

        self._centre_line_vals = (0, 0, 0)
        self._centre_anim_vals = (0, 0, 0)

        # Duration of outermost orbit in seconds
        self._orbit_duration = orbit_duration

        self._fig = plt.figure(figsize=(10, 10))
        self._ax = plt.axes(projection="3d")

        self.calculate_line_vals()
        self.calculate_anim_vals()
        self.create_animation()

    def calculate_line_vals(self):
        periods = [float(self.constants.OrbitalPeriod[planet].value) for planet in self._planets]
        time_vals = np.linspace(0, float(max(periods)), 1000)
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
        self._num_frames = round((self._orbit_duration * 1000) / Animation3D.FRAME_DURATION)
        time_vals = np.linspace(0, max_period, self._num_frames)

        if self._centre != self.constants.SUN:
            # Calculates orbital angles at corresponding poins in time
            theta_vals = (2 * math.pi * time_vals) / float(self.constants.OrbitalPeriod[self._centre].value)
            self._centre_anim_vals = CalcFunctions.orbital_vals_3d(theta_vals=theta_vals,
                                                                   planet=self._centre,
                                                                   solar_system=self._solar_system)

        for planet in self._planets:
            theta_vals = (2 * math.pi * time_vals) / float(self.constants.OrbitalPeriod[planet].value)
            x_vals, y_vals, z_vals = CalcFunctions.orbital_vals_3d(theta_vals=theta_vals,
                                                                   planet=planet,
                                                                   solar_system=self._solar_system)
            self._anim_data[planet] = (x_vals - self._centre_anim_vals[0],
                                       y_vals - self._centre_anim_vals[1],
                                       z_vals - self._centre_anim_vals[2])

    def init_func(self):
        for line in self._anims:
            line.set_xdata([])
            line.set_ydata([])
            line.set_3d_properties([])
        return self._lines + self._anims

    def animate(self, i):
        for j in range(len(self._planets)):
            current_planet = self._planets[j]
            current_x = self._anim_data[current_planet][0][i]
            current_y = self._anim_data[current_planet][1][i]
            current_z = self._anim_data[current_planet][2][i]
            self._anims[j].set_xdata([current_x])
            self._anims[j].set_ydata([current_y])
            self._anims[j].set_3d_properties([current_z])
        return self._lines + self._anims

    def create_animation(self):
        self._ax.set_box_aspect((3, 3, 1))
        self._ax.view_init(-335.38, 79.14)

        # Initialises line objects for orbital paths and points
        for planet in self._planets:
            self._anims.append(self._ax.plot([], [], [], "ro")[0])
            self._lines.append(self._ax.plot(self._line_data[planet][0],
                                             self._line_data[planet][1],
                                             self._line_data[planet][2],
                                             lw=3)[0])

        ani = FuncAnimation(self._fig,
                            self.animate,
                            frames=self._num_frames,
                            interval=Animation3D.FRAME_DURATION,
                            repeat=True,
                            blit=True,
                            init_func=self.init_func)
        plt.show()
        #ani.save("3d_animation.gif", fps=25)

if __name__ == "__main__":
    Animation3D("HD_219134",["b", "c"], "HD_219134", 3)