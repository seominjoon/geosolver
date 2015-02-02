from collections import namedtuple

__author__ = 'minjoon'

HoughLineParameters = namedtuple("HoughLineParameters",
                                 "rho theta threshold max_gap min_length nms_rho nms_theta max_num")

hough_line_parameters = HoughLineParameters()

HoughCircleParameters = namedtuple("HoughCircleParameters",
                                   "dp minRadius maxRadius param1 param2 minDist max_gap min_length max_num")

hough_circle_parameters = HoughCircleParameters()

PRIMITIVE_SELECTION_LINE_EPS = 2
PRIMITIVE_SELECTION_CIRCLE_EPS = 3
PRIMITIVE_SELECTION_MIN_GAIN = 10
