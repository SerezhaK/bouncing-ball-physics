import matplotlib

matplotlib.use('TkAgg')  # 'tkAgg' if Qt not present
import matplotlib.pyplot as plt
import scipy as sp
import matplotlib.animation as animation
import numpy as np
from scipy import linalg


class Ball:
    def __init__(
            self,
            coefficient_k,
            coefficient_e,
            speed_angular_w=10,
            speed_x_u=0.09,
            speed_y_v=0.1,
            radius=0.08,
            dt=0.01
    ):
        self.x_cord = 0
        self.y_cord = 10
        self.radius = radius

        self.speed_angular_w = speed_angular_w
        self.speed_x_u = speed_x_u
        self.speed_y_v = speed_y_v

        self.coefficient_k = coefficient_k  # ranging from -1 to 1
        self.coefficient_e = coefficient_e  # ranging from 0 to 1

        self.g = 9.81
        self.dt = dt
        self.trajectory = [self.cartesian()]

    def hit_the_floor(self):
        radius = self.radius
        angular = self.speed_angular_w
        x_speed = self.speed_x_u
        y_speed = self.speed_y_v
        k_koef = self.coefficient_k
        e_koef = self.coefficient_e

        a1 = np.array([
            [1, -0.4 * radius, 0],
            [0, 0, 1],
            [1, radius, 0]
        ])
        a2 = np.array([
            [x_speed - 0.4 * radius * angular],
            [-e_koef * y_speed],
            [k_koef * (x_speed + radius * angular)]
        ])
        ans = linalg.solve(a1, a2)
        self.speed_x_u = ans[0][0]
        self.speed_angular_w = ans[1][0]
        self.speed_y_v = ans[2][0]
        print("IMPACT ON THE FLOOR")
        self.y_cord = 0.0000001

    def cartesian(self):
        self.x_cord = self.x_cord + self.speed_x_u
        self.y_cord = self.y_cord + self.speed_y_v

        print(self.x_cord, self.y_cord)
        return sp.array([[self.x_cord, self.y_cord]])

    def evolve(self):
        radius = self.radius
        angular = self.speed_angular_w
        x_speed = self.speed_x_u
        k_koef = self.coefficient_k
        e_koef = self.coefficient_e
        g = self.g

        self.speed_y_v -= g / 1000

        if self.y_cord <= 0:
            self.hit_the_floor()

        new_position = self.cartesian()
        self.trajectory.append(new_position)
        return new_position


class Animator:
    def __init__(self, ball, draw_trace=False):
        self.animation = None
        self.ball = ball
        self.draw_trace = draw_trace
        self.time = 0.0

        # set up the figure
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(-50, 50)
        self.ax.set_ylim(0, 40)

        # prepare a text window for the timer
        self.time_text = self.ax.text(
            0.05,
            0.95,
            '',
            horizontalalignment='left',
            verticalalignment='top',
            transform=self.ax.transAxes
        )
        # initialize by plotting the last position of the trajectory
        self.line, = self.ax.plot(
            self.ball.trajectory[0][0],
            marker='o')

        # trace the whole trajectory of the second ball mass
        if self.draw_trace:
            self.trace, = self.ax.plot(
                [a[0][0] for a in self.ball.trajectory])

    def advance_time_step(self):
        while True:
            self.time += self.ball.dt
            yield self.ball.evolve()

    def update(self, data):
        self.time_text.set_text('Elapsed time: {:6.2f} s'.format(self.time))

        self.line.set_ydata(data[:, 1])
        self.line.set_xdata(data[:, 0])

        if self.draw_trace:
            self.trace.set_xdata([a[0][0] for a in self.ball.trajectory])
            self.trace.set_ydata([a[0][1] for a in self.ball.trajectory])
        return self.line,

    def animate(self):
        self.animation = animation.FuncAnimation(
            self.fig,
            func=self.update,
            frames=self.advance_time_step,
            interval=25,
            blit=False,
            repeat=False
        )


ball = Ball(
    dt=0.01,
    coefficient_e=0.6,
    coefficient_k=0.4
)
animator = Animator(
    ball=ball,
    draw_trace=True
)
animator.animate()
plt.show()
