import numpy as np
from geosolver.diagram.computational_geometry import distance_between_line_and_point, line_length, \
    distance_between_points, intersections_between_lines, line_vector, angle_in_radian
from geosolver.ontology.instantiator_definitions import instantiators

__author__ = 'minjoon'

class TruthValue(object):
    def __init__(self, value, std=None):
        self.norm = value
        self.conf = np.exp(-self.norm)

    def __add__(self, other):
        return TruthValue(self.norm + other.norm)

    def __repr__(self):
        return "TruthValue(%.2f)" % self.norm

def Line(p1, p2):
    return instantiators['line'](p1, p2)

def Circle(p, r):
    return instantiators['circle'](p, r)

def Point(x, y):
    return instantiators['point'](x, y)

def Angle(a, b, c):
    return instantiators['angle'](a, b, c)

def LengthOf(line):
    return line_length(line)

def RadiusOf(circle):
    return circle.radius

def Equals(a, b):
    std = abs((a+b)/2.0)
    value = abs(a-b)
    return TruthValue(value, std)

def Greater(a, b):
    std = abs((a+b)/2.0)
    value = max(b-a, 0)
    return TruthValue(value, std)

def Less(a, b):
    std = abs((a+b)/2.0)
    value = max(a-b, 0)
    return TruthValue(value, std)

def Tangent(line, circle):
    d = distance_between_line_and_point(line, circle.center)
    return Equals(d, circle.radius)

def IsDiameter(line, circle):
    return IsChord(line, circle) + Equals(LengthOf(line), 2*circle.radius)

def PointLiesOnCircle(point, circle):
    d = distance_between_points(point, circle.center)
    return Equals(d, circle.radius)

def IsChord(line, circle):
    return PointLiesOnCircle(line.a, circle) + PointLiesOnCircle(line.b, circle)

def Perpendicular(l1, l2):
    return Equals((l1.b.y-l1.a.y)*(l2.b.y-l2.a.y), (l1.a.x-l1.b.x)*(l2.b.x-l2.a.x))

def Colinear(A, B, C):
    return Equals((B.y - A.y) * (C.x - B.x), (B.x - A.x) * (C.y - B.y))

def PointLiesOnLine(point, line):
    return Colinear(line.a, point, line.b) + Equals(LengthOf(line), distance_between_points(line.a, point) + distance_between_points(line.b, point))


