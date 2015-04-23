from geosolver.diagram.computational_geometry import line_length
from geosolver.ontology.states import Truth

__author__ = 'minjoon'

def equal(a, b):
    """
    Equality between a and b

    :param float a:
    :param float b:
    :return float:
    """
    value = abs(a - b)
    sig = abs(a + b) / 2
    return Truth(value, sig)


def lengthOf(line):
    return line_length(line)


def radiusOf(circle):
    return circle.radius