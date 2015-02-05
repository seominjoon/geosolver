import numpy as np
from geosolver.ontology.instantiator_definitions import instantiators

__author__ = 'minjoon'

def distance_between_points(p0, p1):
    return np.linalg.norm(dimension_wise_distance_between_points(p0, p1))


def distance_between_points_squared(p0, p1):
    return (p0.x-p1.x)**2 + (p0.y-p1.y)**2


def dimension_wise_distance_between_points(p0, p1):
    return abs(p0.x-p1.x), abs(p0.y-p1.y)


def dot_distance_between_points(unit_vector, point, reference_point):
    """
    Distance between two points dot-producted by the unit vector

    :param line:
    :param point:
    :param reference_point:
    :return:
    """
    return np.dot(unit_vector, np.array(point) - np.array(reference_point))


def line_length(line):
    return distance_between_points(line.a, line.b)


def line_unit_vector(line):
    array = (np.array(line[1]) - np.array(line[0]))/line_length(line)
    return tuple(array)


def line_normal_vector(line):
    unit_vector = line_unit_vector(line)
    return unit_vector[1], -unit_vector[0]


def circumference(circle):
    return 2*np.pi*circle.radius


def midpoint(p0, p1):
    return instantiators['point'](*((np.array(p0) + np.array(p1))/2.0))


def distance_between_line_and_point(line, point):
    """
    This function is slow... Please improve!

    :param line:
    :param point:
    :return:
    """
    p = midpoint(line.a, line.b)
    vector = point.x - p.x, point.y - p.y
    u = line_unit_vector(line)
    n = line_normal_vector(line)
    perpendicular_distance = abs(np.dot(vector, n))
    parallel_distance = abs(np.dot(vector, u))
    if parallel_distance <= line_length(line)/2.0:
        return perpendicular_distance
    else:
        return min(distance_between_points(point, line.a),
                   distance_between_points(point, line.b))


def distance_between_circle_and_point(circle, point):
    return abs(circle.radius - distance_between_points(circle.center, point))

