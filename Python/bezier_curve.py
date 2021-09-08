# import
import numpy as np
import matplotlib.pyplot as plt

# def


def linear_bezier_curve(number_of_t, p0, p1):
    points = []
    for t in np.linspace(0, 1, number_of_t):
        (p0*(1-t)**2)+(2*t*(1-t)*p1)+((t**2)*p2)
        points.append(((1-t)*p0)+(t*p1))
    points = np.array(points)
    return points


def quadratic_bezier_curve(number_of_t, p0, p1, p2):
    points = []
    for t in np.linspace(0, 1, number_of_t):
        points.append((p0*(1-t)**2)+(2*t*(1-t)*p1)+((t**2)*p2))
    points = np.array(points)
    return points


def cubic_bezier_curve(number_of_t, p0, p1, p2, p3):
    points = []
    for t in np.linspace(0, 1, number_of_t):
        points.append((p0*(1-t)**3)+(3*p1*t*(1-t)**2) +
                      (3*p2*(t**2)*(1-t))+(p3*t**3))
    points = np.array(points)
    return points


if __name__ == '__main__':
    # parameters
    p0 = np.array([0, 0])
    p1 = np.array([2, 4])
    p2 = np.array([5, 3])
    p3 = np.array([6, 6])
    number_of_t = 100

    # get bezier curve
    linear_points = linear_bezier_curve(number_of_t=number_of_t, p0=p0, p1=p1)
    quadratic_points = quadratic_bezier_curve(
        number_of_t=number_of_t, p0=p0, p1=p1, p2=p2)
    cubic_points = cubic_bezier_curve(
        number_of_t=number_of_t, p0=p0, p1=p1, p2=p2, p3=p3)

    # display curve
    plt.plot(linear_points[:, 0], linear_points[:, 1],
             label='linear_bezier_curve')
    plt.plot(quadratic_points[:, 0], quadratic_points[:,
                                                      1], label='quadratic_bezier_curve')
    plt.plot(cubic_points[:, 0], cubic_points[:, 1],
             label='cubic_bezier_curve')
    plt.scatter(p0[0], p0[1], label='p0')
    plt.scatter(p1[0], p1[1], label='p1')
    plt.scatter(p2[0], p2[1], label='p2')
    plt.scatter(p3[0], p3[1], label='p3')
    plt.legend()
    plt.show()
