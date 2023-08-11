import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from solar_system_constants import *
import numpy as np
import math

matplotlib.use('TkAgg')


class Animation3D:
    FRAME_DURATION = 40

    def __init__(self, planets: list[str], centre: str, orbit_duration: float):
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
        theta = np.linspace(0, 2 * math.pi, 100)

        # Generates points for orbital path of every planet at regular intervals in orbital angle
        if self._centre != Planet.SUN.name:
            angle_centre = InclinationAngle[self._centre].value
            b_centre = SemiMinorAxis[self._centre].value
            e_centre = Eccentricity[self._centre].value
            r_centre = float(b_centre) / (1 - float(e_centre) * np.cos(theta))
            x_centre = r_centre * np.cos(theta) * np.cos(angle_centre)
            y_centre = r_centre * np.sin(theta)
            z_centre = x_centre * np.sin(angle_centre)
            self._centre_line_vals = (x_centre, y_centre, z_centre)

        for planet in self._planets:
            angle = InclinationAngle[planet].value
            b = SemiMinorAxis[planet].value
            e = Eccentricity[planet].value
            r = float(b) / (1 - float(e) * np.cos(theta))
            x = r * np.cos(theta) * np.cos(angle)
            y = r * np.sin(theta)
            z = x * np.sin(angle)

            # Subtracts coordinates of reference planet at each corresponding orbital angle
            self._line_data[planet] = (x - self._centre_line_vals[0],
                                       y - self._centre_line_vals[1],
                                       z - self._centre_line_vals[2])

    def calculate_anim_vals(self):
        periods = [OrbitalPeriod[planet].value for planet in self._planets]
        max_period = max(periods)

        # Calculates total number of frames that will make up animation
        self._num_frames = round((self._orbit_duration * 1000) / Animation3D.FRAME_DURATION)
        time_vals = np.linspace(0, max_period, self._num_frames)

        if self._centre != Planet.SUN.name:
            # Calculates orbital angles at corresponding poins in time
            theta_vals = (2 * math.pi * time_vals) / float(OrbitalPeriod[self._centre].value)
            angle_centre = InclinationAngle[self._centre].value
            b_centre = SemiMinorAxis[self._centre].value
            e_centre = Eccentricity[self._centre].value
            r_centre = float(b_centre) / (1 - float(e_centre) * np.cos(theta_vals))
            x_centre = r_centre * np.cos(theta_vals) * np.cos(angle_centre)
            y_centre = r_centre * np.sin(theta_vals)
            z_centre = x_centre * np.sin(angle_centre)
            self._centre_anim_vals = (x_centre, y_centre, z_centre)

        for planet in self._planets:
            theta_vals = (2 * math.pi * time_vals) / float(OrbitalPeriod[planet].value)
            angle = InclinationAngle[planet].value
            b = SemiMinorAxis[planet].value
            e = Eccentricity[planet].value
            r = float(b) / (1 - float(e) * np.cos(theta_vals))
            x = r * np.cos(theta_vals) * np.cos(angle)
            y = r * np.sin(theta_vals)
            z = x * np.sin(angle)
            self._anim_data[planet] = (x - self._centre_anim_vals[0],
                                       y - self._centre_anim_vals[1],
                                       z - self._centre_anim_vals[2])

    def init_func(self):
        for line in self._anims:
            line.set_data([], [], [])
        return self._lines + self._anims

    def animate(self, i):
        for j in range(len(self._planets)):
            current_planet = self._planets[j]
            current_x = self._anim_data[current_planet][0][i]
            current_y = self._anim_data[current_planet][1][i]
            current_z = self._anim_data[current_planet][2][i]
            self._anims[j].set_data([current_x], [current_y], [current_z])
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
        ani.save("3d_animation.gif", fps=25)