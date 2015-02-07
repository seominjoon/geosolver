import cv2
import numpy as np
from geosolver.diagram.computational_geometry import cartesian_angle
from geosolver.ontology.instantiator_definitions import instantiators
from geosolver.utils import round_vector

__author__ = 'minjoon'


def draw_instance(image, instance, **kwargs):
    for key, instantiator in instantiators.iteritems():
        if isinstance(instance, instantiator):
            eval("draw_%s(image, instance, **kwargs)" % key)

def draw_line(image, line, offset=(0, 0), color=(0, 0, 255), thickness=1):
    pt1 = round_vector(np.array(line.a) + offset)
    pt2 = round_vector(np.array(line.b) + offset)
    cv2.line(image, pt1, pt2, color, thickness=thickness)


def draw_circle(image, circle, offset=(0, 0), color=(0, 0, 255), thickness=1):
    center = round_vector(np.array(circle.center) + offset)
    cv2.circle(image, center, circle.radius, color, thickness=thickness)


def draw_point(image, point, offset=(0, 0), color=(0, 255, 0), thickness=1, radius=1):
    circle = instantiators['circle'](point, radius)
    draw_circle(image, circle, offset=offset, color=color, thickness=thickness)


def draw_arc(image, arc, offset=(0, 0), color=(0, 0, 255), thickness=1):
    caa = cartesian_angle(arc.circle.center, arc.a) * 180/np.pi
    cab = cartesian_angle(arc.circle.center, arc.b) * 180/np.pi
    center = tuple(round_vector(np.array(arc.circle.center) + offset))
    radius = int(round(arc.circle.radius))
    cv2.ellipse(image, center, (radius, radius), 0, caa, cab, color, thickness)



