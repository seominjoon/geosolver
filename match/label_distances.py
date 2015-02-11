from geosolver.diagram.computational_geometry import distance_between_points, midpoint, cartesian_angle, \
    signed_distance_between_cartesian_angles, arc_midpoint

__author__ = 'minjoon'


def label_distance_to_line_length(label_point, line):
    """
    distance from midpoint of line

    :param point:
    :param line:
    :return:
    """
    mp = midpoint(line.a, line.b)
    return distance_between_points(label_point, mp)


def label_distance_to_line(label_point, line):
    """
    minimum distance among:
    end points, mid point.

    :param point:
    :param line:
    :return:
    """
    return min(label_distance_to_line_length(label_point, line),
               distance_between_points(label_point, line.a),
               distance_between_points(label_point, line.b))


def label_distance_to_arc(label_point, arc):
    return distance_between_points(label_point, arc_midpoint(arc))


def label_distance_to_angle(label_point, angle):
    """
    If outside of the convex area, then distance is very high.
    :param point:
    :param angle:
    :return:
    """
    caa = cartesian_angle(angle.b, angle.a)
    cam = cartesian_angle(angle.b, label_point)
    cab = cartesian_angle(angle.b, angle.c)
    dm = signed_distance_between_cartesian_angles(caa, cam)
    db = signed_distance_between_cartesian_angles(caa, cab)
    dist = distance_between_points(label_point, angle.b)
    if db > dm:
        return dist
    else:
        return 4*dist  # effectively infinite


def label_distance_to_point(label_point, point):
    return distance_between_points(label_point, point)