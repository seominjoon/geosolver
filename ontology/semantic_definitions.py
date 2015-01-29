"""
Semantic definitions of ontology.

All functions need to be defined in terms of sympy's symbolic representations.
See ontology/basic_definitions.py for ontology.
If the function needs to return a truth value, then it must return an instance of 'Truth'.
Otherwise, it returns a sympy expression (can be a constant).
"""
from collections import namedtuple
import sympy

__author__ = 'minjoon'

type_defs = {
    'point': (('x', 'number'), ('y', 'number')),
    'line': (('a', 'point'), ('b', 'point')),
    'angle': (('a', 'point'), ('b', 'point'), ('c', 'point')),
    'circle': (('center', 'point'), ('radius', 'number')),
    'arc': (('circle', 'circle'), ('a', 'point'), ('b', 'point')),
    'triangle': (('a', 'point'), ('b', 'point'), ('c', 'point')),
    'quadrilateral': (('a', 'point'), ('b', 'point'), ('c', 'point'), ('d', 'point')),
}

"""
Initialize types based on type_defs
"""
types = {}
for key, value in type_defs.iteritems():
    args, _ = zip(*value)
    nt = namedtuple(key, ' '.join(args))
    types[key] = nt


"""
Function Semantics
"""


class Truth(object):
    def __init__(self, expression, sigma):
        """
        Expression, when evaluated, indicates the truth-ness,
        being certain if 0 or less and uncertain if positive.
        Sigma is the rough prediction of the variance of the expression.

        For instance, we might assign 100% probability for expression <= 0,
        and 0% (or 50%; it doesn't really matter) probability for expression >= sigma.
        We can linearly interpolate in the middle.

        For concrete example, see 'equal' function below.
        """
        self.expression = expression
        self.sigma = sigma


def add(number0, number1):
    return number0 + number1


def sub(number0, number1):
    return number0 - number1


def mul(number0, number1):
    return number0 * number1


def div(number0, number1):
    return number0 / number1


def pow(number0, number1):
    return number0 ** number1


def equal(number0, number1):
    expr = sympy.abs(number0 - number1)
    sig = (number0 + number1) / 2
    return Truth(expr, sig)


def greater(number0, number1):
    expr = number1 - number0
    sig = (number0 + number1) / 2
    return Truth(expr, sig)


def less(number0, number1):
    expr = number0 - number1
    sig = (number0 + number1) / 2
    return Truth(expr, sig)


def lengthOf(line):
    return sympy.sqrt((line.a.x-line.b.x)**2 + (line.a.y-line.b.y)**2)


def angleOf_angle(angle):
    a = lengthOf(types['line'](angle.b, angle.c))
    b = lengthOf(types['line'](angle.c, angle.a))
    c = lengthOf(types['line'](angle.a, angle.b))
    return sympy.sqrt((a**2 + b**2 - c**2) / (2*a*b))


def angleOf_arc(arc):
    angle = types['angle'](arc.a, arc.circle.center, arc.b)
    return angleOf_angle(angle)


def radiusOf(circle):
    return circle.radius


def diameterOf(circle):
    return 2 * circle.radius


def areaOf_polygon(polygon):
    """
    TO BE IMPLEMENTED
    :param polygon:
    :return:
    """
    pass


def areaOf_circle(circle):
    return sympy.pi * circle.radius**2


def perimeterOf(polygon):
    lines = [types['line'](polygon[idx-1], polygon[idx]) for idx in len(polygon)]
    return sum(lengthOf(line) for line in lines)


def circumferenceOf(circle):
    return 2 * sympy.pi * circle.radius


def intersects(entity0, entity1):
    """
    TO BE IMPLEMENTED
    :param entity0:
    :param entity1:
    :return:
    """
    if isinstance(entity0, types['line']):
        pass


def isOn(point, entity):
    """
    TO BE IMPLEMENTED
    :param point:
    :param entity:
    :return:
    """
    if isinstance(entity, types['line']):
        pass
    elif isinstance(entity, types['circle']):
        pass


def isMidpointOf(point, line):
    a = lengthOf(types['line'](line.a, point))
    b = lengthOf(types['line'](point, line.b))
    return equal(a, b)


# And so on...