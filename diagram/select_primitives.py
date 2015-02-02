from geosolver.diagram.states import PrimitiveParse
from geosolver.ontology.utils import line_length, circumference, distance_between_line_and_point, \
    distance_between_circle_and_point
from geosolver.ontology.instantiator_definitions import instantiators
import numpy as np
import geosolver.parameters as params

__author__ = 'minjoon'


def select_primitives(primitive_parse):
    assert isinstance(primitive_parse, PrimitiveParse)
    pixels_dict = _get_pixels_dict(primitive_parse,
                                   params.PRIMITIVE_SELECTION_LINE_EPS, params.PRIMITIVE_SELECTION_CIRCLE_EPS)
    selected_primitives = {}
    remaining_primitives = primitive_parse.primitives.copy()
    reward = 0
    while True:
        key = _get_next_primitive_key(selected_primitives, remaining_primitives, pixels_dict)
        updated_selected_primitives = selected_primitives.copy()
        updated_selected_primitives[key] = remaining_primitives[key]
        new_reward = _evaluate_reward(updated_selected_primitives, pixels_dict)
        if new_reward - reward > params.PRIMITIVE_SELECTION_MIN_GAIN:
            selected_primitives = updated_selected_primitives
            reward = new_reward
        else:
            break

    lines = dict(pair for pair in selected_primitives.iteritems()
                 if isinstance(pair[1], instantiators['line']))
    circles = dict(pair for pair in selected_primitives.iteritems()
                   if isinstance(pair[1], instantiators['circle']))
    new_primitive_parse = PrimitiveParse(primitive_parse.image_segment_parse, lines, circles)
    return new_primitive_parse


def _get_next_primitive_key(selected_primitives, remaining_primitives, pixels_dict):
    return max(remaining_primitives.items(),
               key=lambda p: _evaluate_reward(selected_primitives.values()+[p[1]], pixels_dict))[0]


def _get_pixels_dict(primitive_parse, line_eps, circle_eps):
    primitives = primitive_parse.primitives
    pixels = primitive_parse.image_segment_parse.diagram_image_segment.pixels
    pixels_dict = {}
    for key, primitive in primitives.iteritems():
        if isinstance(primitive, instantiators['line']):
            f = distance_between_line_and_point
            eps = line_eps
        elif isinstance(primitive, instantiators['circle']):
            f = distance_between_circle_and_point
            eps = circle_eps
        curr_pixels = set(pixel for pixel in pixels if f(primitive, pixel) < eps)
        pixels_dict[key] = curr_pixels
    return pixels_dict


def _evaluate_reward(partial_primitives, pixels_dict):
    x = [_coverage(partial_primitives, pixels_dict),
         _pixel_num(partial_primitives, pixels_dict),
         _length(partial_primitives),
         ]
    w = [1, -0.2, -0.2]
    return np.dot(x, w)


def _coverage(partial_primitives, pixels_dict):
    if len(partial_primitives) == 0:
        return 0
    coverage = len(set.union(*[pixels_dict[key] for key in partial_primitives]))
    return coverage


def _pixel_num(partial_primitives, pixels_dict):
    if len(partial_primitives) == 0:
        return 0
    num = sum(len(pixels_dict[key]) for key in partial_primitives)
    return num


def _length(partial_primitives):
    if len(partial_primitives) == 0:
        return 0
    total = 0
    for primitive in partial_primitives.values():
        if isinstance(primitive, instantiators['line']):
            total += line_length(primitive)
        elif isinstance(primitive, instantiators['circle']):
            total += circumference(primitive)
        else:
            raise Exception()
    return total


def _coherence(partial_primitives):
    scores = []
    for idx, primitive in partial_primitives.iteritems():
        if isinstance(primitive, instantiators['line']):
            score = _line_coherence(partial_primitives, idx)
        elif isinstance(primitive, instantiators['circle']):
            score = _circle_coherence(partial_primitives, idx)
        scores.append(score)
    return np.mean(scores)


def _line_coherence(partial_primitives, curr_idx):
    return 0


def _circle_coherence(partial_primitives, curr_idx):
    return 0