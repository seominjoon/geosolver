import itertools
from geosolver.diagram.computational_geometry import distance_between_points, distance_between_line_and_point, \
    distance_between_circle_and_point, distance_between_arc_and_point
from geosolver.diagram.instance_exists import instance_exists
from geosolver.diagram.states import CoreParse, GraphParse
import networkx as nx
from geosolver.ontology.instantiator_definitions import instantiators
from geosolver.parameters import LINE_EPS, CIRCLE_EPS

__author__ = 'minjoon'


def parse_graph(core_parse):
    assert isinstance(core_parse, CoreParse)
    circle_dict = _get_circle_dict(core_parse)
    line_graph = _get_line_graph(core_parse)
    arc_graphs = {}
    for center_key, d in circle_dict.iteritems():
        for radius_key in d:
            circle = circle_dict[center_key][radius_key]['instance']
            points = circle_dict[center_key][radius_key]['points']
            arc_graphs[(center_key, radius_key)] = _get_arc_graph(core_parse, circle, points)

    graph_parse = GraphParse(core_parse, line_graph, circle_dict, arc_graphs)
    return graph_parse


def _get_circle_dict(diagram_parse):
    """
    A dictionary of dictionaries, where key of the top dictionary is center point.
    The bottom dictionary contains radii (if multiple circles exist with the same center).

    :param diagram_parse:
    :return:
    """
    # FIXME : this needs to be changed
    eps = CIRCLE_EPS
    assert isinstance(diagram_parse, CoreParse)
    circle_dict = {}


    for point_key, point in diagram_parse.intersection_points.iteritems():
        d = {}
        radius_key = 0
        for circle in diagram_parse.primitive_parse.circles.values():
            if distance_between_points(point, circle.center) <= eps:
                points = {}
                for key in diagram_parse.intersection_points:
                    point = diagram_parse.intersection_points[key]
                    if distance_between_circle_and_point(circle, point) <= eps:
                        points[key] = point
                d[radius_key] = {'instance': circle, 'points': points}
                radius_key += 1
        if len(d) > 0:
            circle_dict[point_key] = d
    return circle_dict



def _get_line_graph(diagram_parse):
    """
    line graph is a non-directional graph.
    Nodes are indexed by intersection points.
    Note that angles, triangles, and quadrilaterals can be parsed from this graph.
    :param diagram_parse:
    :param eps:
    :return:
    """
    eps = LINE_EPS
    line_graph = nx.Graph()

    for key0, key1 in itertools.combinations(diagram_parse.intersection_points, 2):
        p0, p1 = diagram_parse.intersection_points[key0], diagram_parse.intersection_points[key1]
        line = instantiators['line'](p0, p1)
        if instance_exists(diagram_parse, line):
            points = {}
            for key in set(diagram_parse.intersection_points).difference({key0, key1}):
                point = diagram_parse.intersection_points[key]
                if distance_between_line_and_point(line, point) <= eps:
                    points[key] = point
            line_graph.add_edge(key0, key1, instance=line, points=points)
    return line_graph


def _get_arc_graph(diagram_parse, circle, circle_points):
    """
    Directional arc graph.

    :param diagram_parse:
    :param circle:
    :return:
    """
    eps = CIRCLE_EPS
    arc_graph = nx.DiGraph()
    for key0, key1 in itertools.permutations(circle_points, 2):
        p0, p1 = circle_points[key0], circle_points[key1]
        arc = instantiators['arc'](circle, p0, p1)
        if instance_exists(diagram_parse, arc):
            arc_points = {}
            for key in set(circle_points).difference({key0, key1}):
                point = circle_points[key]
                if distance_between_arc_and_point(arc, point) <= eps:
                    arc_points[key] = point
            arc_graph.add_edge(key0, key1, instance=arc, points=arc_points)
    return arc_graph


