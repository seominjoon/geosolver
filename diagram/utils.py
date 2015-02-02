import cv2
import numpy as np
from geosolver.utils import round_vector

__author__ = 'minjoon'


def draw_line(image, line, offset=(0,0), color=(0, 0, 255), thickness=1):
    pt1 = round_vector(np.array(line.a) + offset)
    pt2 = round_vector(np.array(line.b) + offset)
    cv2.line(image, pt1, pt2, color, thickness=thickness)


def draw_circle(image, circle, offset=(0,0), color=(0, 0, 255), thickness=1):
    center = round_vector(np.array(circle.center) + offset)
    cv2.circle(image, center, circle.radius, color, thickness=thickness)



