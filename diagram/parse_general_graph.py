import copy
from geosolver.diagram.states import GraphParse, GeneralGraphParse
from geosolver.diagram.states import GeneralDiagramParse
from geosolver.ontology.instantiator_definitions import instantiators

__author__ = 'minjoon'


def parse_general_graph(general_diagram_parse, graph_parse):
    """
    For each edge, change instances.

    :param general_diagram_parse:
    :param graph_parse:
    :return:
    """
    assert isinstance(general_diagram_parse, GeneralDiagramParse)
    assert isinstance(graph_parse, GraphParse)
    # FIXME : circle dict needs to be changed
    circle_dict = copy.deepcopy(graph_parse.circle_dict)
    line_graph = graph_parse.line_graph.copy()
    arc_graphs = {key: arc_graph.copy() for key, arc_graph in graph_parse.arc_graphs.iteritems()}
    points = general_diagram_parse.intersection_points

    for center_key, d in circle_dict.iteritems():
        for radius_key, dd in d.iteritems():
            dd['instance'] = general_diagram_parse.circles[center_key][radius_key]

    for a_key, b_key in line_graph.edges():
        instance = instantiators['line'](points[a_key], points[b_key])
        line_graph[a_key][b_key]['instance'] = instance

    for (center_key, radius_key), arc_graph in arc_graphs.iteritems():
        circle = general_diagram_parse.circles[center_key][radius_key]
        for a_key, b_key in arc_graph.edges():
            instance = instantiators['arc'](circle, points[a_key], points[b_key])
            arc_graph[a_key][b_key]['instance'] = instance

    general_graph_parse = GeneralGraphParse(general_diagram_parse, graph_parse, line_graph, circle_dict, arc_graphs)
    return general_graph_parse