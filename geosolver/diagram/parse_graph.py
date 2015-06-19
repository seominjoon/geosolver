import itertools
from geosolver.diagram.computational_geometry import distance_between_points, distance_between_line_and_point, \
    distance_between_circle_and_point, distance_between_arc_and_point
from geosolver.diagram.instance_exists import instance_exists
from geosolver.diagram.states import CoreParse, GraphParse
import networkx as nx
from geosolver.ontology.instantiator_definitions import instantiators
from geosolver.ontology.ontology_semantics import evaluate
from geosolver.parameters import LINE_EPS, CIRCLE_EPS
from geosolver.text2.ontology import FunctionNode, function_signatures

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

    confident_variable_nodes = _temp(core_parse, circle_dict, line_graph)

    graph_parse = GraphParse(core_parse, line_graph, circle_dict, arc_graphs, confident_variable_nodes)
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
            for key in set(circle_points).difference(set([key0, key1])):
                point = circle_points[key]
                if distance_between_arc_and_point(arc, point) <= eps:
                    arc_points[key] = point
            arc_graph.add_edge(key0, key1, instance=arc, points=arc_points)
    return arc_graph


def _temp(core_parse, circle_dict, line_graph):
    confident_variable_nodes = []

    for from_key, to_key, data in line_graph.edges(data=True):
        line_variable = FunctionNode(function_signatures['Line'],
                                     [core_parse.point_variables[from_key], core_parse.point_variables[to_key]])
        points = data['points']
        for point_key, point in points.iteritems():
            point_variable = core_parse.point_variables[point_key]
            variable_node = FunctionNode(function_signatures['PointLiesOnLine'], [point_variable, line_variable])
            confident_variable_nodes.append(variable_node)

    for center_key, d in circle_dict.iteritems():
        for radius_key, dd in d.iteritems():
            circle_variable = FunctionNode(function_signatures['Circle'],
                                           [core_parse.point_variables[center_key],
                                            core_parse.radius_variables[center_key][radius_key]])
            points = dd['points']
            for point_key, point in points.iteritems():
                point_variable = core_parse.point_variables[point_key]
                variable_node = FunctionNode(function_signatures['PointLiesOnCircle'], [point_variable, circle_variable])
                confident_variable_nodes.append(variable_node)

    return confident_variable_nodes



def _get_confident_variable_nodes(core_parse, circle_dict, line_graph):
    assert isinstance(core_parse, CoreParse)
    confident_variable_nodes = []

    # Get point-lies-on-line function nodes
    for from_key, to_key, data in line_graph.edges(data=True):
        line = data['instance']
        line_variable = FunctionNode(function_signatures['Line'],
                                     [core_parse.point_variables[from_key], core_parse.point_variables[to_key]])
        for mid_key, point in core_parse.intersection_points.iteritems():
            if mid_key == from_key or mid_key == to_key:
                continue
            point_variable = core_parse.point_variables[mid_key]
            function_node = FunctionNode(function_signatures['PointLiesOnLine'], [point, line])
            variable_node = FunctionNode(function_signatures['PointLiesOnLine'], [point_variable, line_variable])
            confidence = evaluate(function_node, core_parse.variable_assignment).conf
            if confidence > 0.5:
                confident_variable_nodes.append(variable_node)

    # Get point-lies-on-circle function nodes
    for center_key, d in circle_dict.iteritems():
        for radius_key, dd in d.iteritems():
            circle = dd['instance']
            circle_variable = FunctionNode(function_signatures['Circle'],
                                           [core_parse.point_variables[center_key],
                                            core_parse.radius_variables[center_key][radius_key]])
            for point_key, point in core_parse.intersection_points.iteritems():
                point_variable = core_parse.point_variables[point_key]
                function_node = FunctionNode(function_signatures['PointLiesOnCircle'], [point, circle])
                variable_node = FunctionNode(function_signatures['PointLiesOnCircle'], [point_variable, circle_variable])
                confidence = evaluate(function_node, core_parse.variable_assignment).conf
                if confidence > 0.5:
                    confident_variable_nodes.append(variable_node)

    return confident_variable_nodes
