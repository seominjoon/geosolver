import sympy
from geosolver.ontology.instantiator_definitions import instantiators
from geosolver.ontology.states import Truth

__author__ = 'minjoon'


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
    sig = sympy.abs(number0 + number1) / 2
    return Truth(expr, sig)


def greater(number0, number1):
    expr = number1 - number0
    sig = sympy.abs(number0 + number1) / 2
    return Truth(expr, sig)


def less(number0, number1):
    expr = number0 - number1
    sig = sympy.abs(number0 + number1) / 2
    return Truth(expr, sig)


def lengthOf(line):
    return sympy.sqrt((line.a.x-line.b.x)**2 + (line.a.y-line.b.y)**2)


def angleOf_angle(angle):
    a = lengthOf(instantiators['line'](angle.b, angle.c))
    b = lengthOf(instantiators['line'](angle.c, angle.a))
    c = lengthOf(instantiators['line'](angle.a, angle.b))
    return sympy.sqrt((a**2 + b**2 - c**2) / (2*a*b))


def angleOf_arc(arc):
    angle = instantiators['angle'](arc.a, arc.circle.center, arc.b)
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
    lines = [instantiators['line'](polygon[idx-1], polygon[idx]) for idx in len(polygon)]
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
    if isinstance(entity0, instantiators['line']):
        pass


def isOn(point, entity):
    """
    TO BE IMPLEMENTED
    :param point:
    :param entity:
    :return:
    """
    if isinstance(entity, instantiators['line']):
        pass
    elif isinstance(entity, instantiators['circle']):
        pass


def isMidpointOf(point, line):
    a = lengthOf(instantiators['line'](line.a, point))
    b = lengthOf(instantiators['line'](point, line.b))
    return equal(a, b)


# And so on...
