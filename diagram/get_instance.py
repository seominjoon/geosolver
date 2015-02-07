from geosolver.ontology.instantiator_definitions import instantiators

__author__ = 'minjoon'

def get_instances(graph_parse, instance_type_name, *args):
    assert instance_type_name in instantiators
    return eval("_get_%s(graph_parse, *args)" % instance_type_name)

def _get_line(graph_parse, a_key, b_key):
    pass

def _get_circles(graph_parse, center_key):
    pass

def _get_circle(graph_parse, center_key, radius_key):
    pass

def _get_arc(graph_parse, circle_key, a_key, b_key):
    """
    :param graph_parse:
    :param circle_key: (center_key, radius_key)
    :param a_key:
    :param b_key:
    :return:
    """

def _get_triangle(graph_parse, a_key, b_key, c_key):
    pass

def _get_quadrilateral(graph_parse, a_key, b_key, c_key, d_key):
    pass

def _get_angle(graph_parse, a_key, b_key, c_key):
    pass