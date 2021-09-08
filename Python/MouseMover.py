# import
from pynput.mouse import Controller
import numpy as np
import random
import time

# class


class MouseMover:
    def __init__(self, screen_width, screen_height, bezier_t, move_time) -> None:
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.bezier_t = bezier_t
        self.move_time = move_time
        self.mouse = Controller()

    def cubic_bezier_curve(self, number_of_t, p0, p1, p2, p3):
        points = []
        for t in np.linspace(0, 1, number_of_t):
            points.append((p0*(1-t)**3)+(3*p1*t*(1-t)**2) +
                          (3*p2*(t**2)*(1-t))+(p3*t**3))
        points = np.array(points)
        return points

    def move(self, x, y):
        p0 = np.array(self.mouse.position)
        p1 = np.array([random.randint(0, self.screen_width),
                       random.randint(0, self.screen_height)])
        p2 = np.array([random.randint(p1[0], self.screen_width),
                       random.randint(p1[1], self.screen_height)])
        p3 = np.array([x, y])
        points = self.cubic_bezier_curve(
            number_of_t=self.bezier_t, p0=p0, p1=p1, p2=p2, p3=p3)
        for point in points:
            print(point)
            self.mouse.position = tuple(point)
            time.sleep(move_time/1000)


if __name__ == '__main__':
    # parameters
    screen_width = 1440
    screen_height = 900
    bezier_t = 50
    move_time = 10  # ms

    # create object
    mouse_mover = MouseMover(screen_width=screen_width, screen_height=screen_height,
                             bezier_t=bezier_t, move_time=move_time)

    # move mouse
    mouse_mover.move(x=100, y=100)
