import numpy as np

import itertools
from geosolver.diagram.computational_geometry import distance_between_line_and_point, line_length, \
    distance_between_points, angle_in_radian, cartesian_angle, signed_distance_between_cartesian_angles, \
    horizontal_angle
from geosolver.ontology.instantiator_definitions import instantiators
from geosolver.ontology.ontology_definitions import FormulaNode, VariableSignature, issubtype, SetNode
import sys
from geosolver.utils.num import is_number
import operator

this = sys.modules[__name__]

__author__ = 'minjoon'

class TruthValue(object):
    def __init__(self, norm, std=None, conf=None):
        if std is not None:
            norm /= std
        self.norm = norm
        if conf is None:
            self.conf = min(0, 1-norm)
        else:
            self.conf = conf

    def __and__(self, other):
        if isinstance(other, TruthValue):
            conf = self.conf
            if self.conf > other.conf:
                conf = other.conf
            norm = (self.norm + other.norm)/2.0
            return TruthValue(norm, conf=conf)
        elif other is True:
            return self
        else:
            raise Exception()

    def __or__(self, other):
        if isinstance(other, TruthValue):
            conf = self.conf
            if self.conf < other.conf:
                conf = other.conf
            norm = self.norm * other.norm
            return TruthValue(norm, conf=conf)
        elif other is True:
            return self
        else:
            raise Exception()

    def __rand__(self, other):
        return self.__and__(other)

    def __ror__(self, other):
        return self.__or__(other)

    def flip(self):
        norm = 1-self.norm
        conf = 1-self.conf
        out = TruthValue(norm, conf=conf)
        return out

    def __repr__(self):
        return "TV(conf=%.2f)" % self.conf

def Line(p1, p2):
    return instantiators['line'](p1, p2)

def Arc(circle, p1, p2):
    return instantiators['arc'](circle, p1, p2)

def Circle(p, r):
    return instantiators['circle'](p, r)

def Point(x, y):
    return instantiators['point'](x, y)

def Angle(a, b, c):
    return instantiators['angle'](a, b, c)

def Triangle(a, b, c):
    return instantiators['triangle'](a, b, c)

def Quad(a, b, c, d):
    return instantiators['quad'](a, b, c, d)

def Hexagon(a, b, c, d, e, f):
    return instantiators['polygon'](a, b, c, d, e, f)

def Polygon(*p):
    return instantiators['polygon'](*p)

def LengthOf(line):
    return line_length(line)

def RadiusOf(circle):
    return circle.radius

def Equals(a, b):
    std = abs((a+b)/2.0)
    value = abs(a-b)
    out = TruthValue(value, std)
    return out

def Greater(a, b):
    std = abs((a+b)/2.0)
    value = max(b-a, 0)
    return TruthValue(value, std)

def Less(a, b):
    std = abs((a+b)/2.0)
    value = max(a-b, 0)
    return TruthValue(value, std)

def Sqrt(x):
    return np.sqrt(x)

def Add(a, b):
    return a + b

def Sub(a, b):
    return a - b

def Mul(a, b):
    return a * b

def Div(a, b):
    return float(a) / b

def Pow(a, b):
    return a**b

def Or(a, b):
    if a.conf > b.conf:
        return a
    return b

def Tangent(line, twod):
    name = twod.__class__.__name__
    if name == "circle":
        d = distance_between_line_and_point(line, twod.center)
        return Equals(d, twod.radius)
    elif issubtype(name, 'polygon'):
        out = reduce(operator.__or__, (PointLiesOnLine(point, line) for point in twod), False)
        return out
    raise Exception()

def IsDiameterLineOf(line, circle):
    return IsChordOf(line, circle) & Equals(LengthOf(line), 2*circle.radius)

def PointLiesOnCircle(point, circle):
    d = distance_between_points(point, circle.center)
    return Equals(d, circle.radius)

def IsChordOf(line, circle):
    return PointLiesOnCircle(line.a, circle) & PointLiesOnCircle(line.b, circle)

def Perpendicular(l1, l2):
    return Equals((l1.b.y-l1.a.y)*(l2.b.y-l2.a.y), (l1.a.x-l1.b.x)*(l2.b.x-l2.a.x))

def Colinear(A, B, C):
    line = instantiators['line'](A, C)
    eq = Equals(LengthOf(line), distance_between_points(line.a, B) + distance_between_points(line.b, B))
    return eq

def PointLiesOnLine(point, line):
    return Colinear(line[0], point, line[1])

def IsMidpointOf(point, line):
    line_a = Line(line.a, point)
    line_b = Line(point, line.b)
    e = Equals(LengthOf(line_a), LengthOf(line_b))
    l = PointLiesOnLine(point, line)
    return e & l

def IsTriangle(triangle):
    if isinstance(triangle, instantiators['triangle']):
        return TruthValue(0)
    else:
        return TruthValue(np.inf)

def IsLine(line):
    if isinstance(line, instantiators['line']):
        return TruthValue(0)
    else:
        return TruthValue(np.inf)

def IsAngle(angle):
    if isinstance(angle, instantiators['angle']):
        return TruthValue(0)
    else:
        return TruthValue(np.inf)

def IsPoint(point):
    if isinstance(point, instantiators['point']):
        return TruthValue(0)
    else:
        return TruthValue(np.inf)

def IsQuad(quad):
    if quad.__class__.__name__ == 'quad':
        return TruthValue(0)
    return TruthValue(np.inf)

def IsInscribedIn(triangle, circle):
    out = reduce(operator.__and__, (PointLiesOnCircle(point, circle) for point in triangle), True)
    return out

def IsCenterOf(point, twod):
    name = twod.__class__.__name__
    if name == 'circle':
        return Equals(point[0], twod.center[0]) & Equals(point[1], twod.center[1])
    elif issubtype(name, 'polygon'):
        distances = [distance_between_points(point, each) for each in twod]
        reg = IsRegular(twod)
        out = reduce(operator.__and__, (Equals(distances[index-1], distance) for index, distance in enumerate(distances)), True)
        return reg & out
    else:
        raise Exception()

def IntersectAt(lines, point):
    assert isinstance(lines, SetNode)
    out = reduce(operator.__and__, (PointLiesOnLine(point, line) for line in lines.children), True)
    return out

def Equilateral(triangle):
    lines = [instantiators['line'](triangle[index-1], point) for index, point in enumerate(triangle)]
    return Equals(LengthOf(lines[0]), LengthOf(lines[1])) & Equals(LengthOf(lines[1]), LengthOf(lines[2]))

def IsSquare(quad):
    lines = [instantiators['line'](quad[index-1], point) for index, point in enumerate(quad)]
    return Equals(LengthOf(lines[0]), LengthOf(lines[1])) & \
           Equals(LengthOf(lines[1]), LengthOf(lines[2])) & Equals(LengthOf(lines[2]), LengthOf(lines[3]))

def AreaOf(twod):
    name = twod.__class__.__name__
    assert issubtype(name, 'twod')
    if name == "circle":
        center, radius = twod
        area = np.pi * radius ** 2
    elif issubtype(name, 'polygon'):
        # http://mathworld.wolfram.com/PolygonArea.html
        area = sum(twod[index-1][0]*p[1]-p[0]*twod[index-1][1] for index, p in enumerate(twod))
    else:
        raise Exception()
    return area

def MeasureOf(angle):
    return angle_in_radian(angle, False)

def IsAreaOf(number, twod):
    return Equals(number, AreaOf(twod))

def IsLengthOf(number, line):
    return Equals(number, LengthOf(line))

def IsPolygon(polygon):
    return TruthValue(0)

def Isosceles(triangle):
    sides = [distance_between_points(triangle[index-1], point) for index, point in enumerate(triangle)]
    combs = itertools.combinations(sides, 2)

    out = reduce(operator.__or__, (Equals(a, b) for a, b in combs), False)
    return out

def BisectsAngle(line, angle):
    on = PointLiesOnLine(angle[1], line)
    distant_point = line[0]
    if distant_point == angle[1]:
        distant_point = line[1]
    a0 = instantiators['angle'](angle[0], angle[1], distant_point)
    a1 = instantiators['angle'](distant_point, angle[1], angle[2])
    eq = Equals(MeasureOf(a0), MeasureOf(a1))
    return on & eq

def Three(entities):
    if len(entities.children) == 3:
        return TruthValue(0)
    return TruthValue(np.inf)

def Two(entities):
    if len(entities.children) == 2:
        return TruthValue(0)
    return TruthValue(np.inf)

def Five(entities):
    if len(entities.children) == 5:
        return TruthValue(0)
    return TruthValue(np.inf)

def Not(truth):
    return truth.flip()


def SumOf(set_node):
    assert isinstance(set_node,SetNode)
    return sum(child for child in set_node.children)

def Parallel(line_0, line_1):
    a0 = cartesian_angle(*line_0)
    a1 = cartesian_angle(*line_1)+np.pi/2
    da = horizontal_angle(signed_distance_between_cartesian_angles(a0, a1))
    return Equals(da, np.pi/2)

def IsTrapezoid(quad):
    lines = _polygon_to_lines(quad)
    out = Parallel(lines[0], lines[2]) | Parallel(lines[1], lines[3])
    return out

def IsRegular(polygon):
    lines = _polygon_to_lines(polygon)
    out = reduce(operator.__and__, (Equals(LengthOf(lines[index-1]), LengthOf(line)) for index, line in enumerate(lines)))
    return out

def IsRectangle(quad):
    angles = (Angle(quad[index-2], quad[index-1], point) for index, point in enumerate(quad))
    out = reduce(operator.__and__, (Equals(MeasureOf(angle), np.pi/2) for angle in angles), True)
    return out

def ValueOf(number):
    return number

def _polygon_to_lines(polygon):
    return [Line(polygon[index-1], point) for index, point in enumerate(polygon)]

def evaluate(function_node, assignment):
    if isinstance(function_node, SetNode):
        assert function_node.head.return_type == 'truth'
        out = reduce(operator.__and__, (evaluate(child, assignment) for child in function_node.children), True)
        return out

    if isinstance(function_node.signature, VariableSignature):
        return assignment[function_node.signature.id]
    elif is_number(function_node.signature.id):
        return float(function_node.signature.id)
    else:
        evaluated_args = []
        for arg in function_node.children:
            if isinstance(arg, FormulaNode):
                evaluated_args.append(evaluate(arg, assignment))
            elif isinstance(arg, SetNode):
                evaluated_args.append(SetNode([evaluate(arg_arg, assignment) for arg_arg in arg.children]))
            else:
                evaluated_args.append(arg)
        return getattr(this, function_node.signature.id)(*evaluated_args)
