from geosolver.diagram.states import DiagramParse

__author__ = 'minjoon'


def parse_graph(diagram_parse):
    assert isinstance(diagram_parse, DiagramParse)


def _get_circle_dict(diagram_parse):
    """
    A dictionary of dictionaries, where key of the top dictionary is center point.
    The bottom dictionary contains radii (if multiple circles exist with the same center).

    :param diagram_parse:
    :return:
    """
    pass

def _get_line_graph(diagram_parse):
    """
    line graph is a non-directional graph.
    Nodes are indexed by intersection points.
    Note that angles, triangles, and quadrilaterals can be parsed from this graph.
    :param diagram_parse:
    :param eps:
    :return:
    """

def _get_arc_graph(diagram_parse, circle):
    """
    Directional arc graph.

    :param diagram_parse:
    :param circle:
    :return:
    """

def _get_points_on_lines(diagram_parse, line_graph):
    pass

def _get_points_on_circles(diagram_parse, circle_dict):
    pass

