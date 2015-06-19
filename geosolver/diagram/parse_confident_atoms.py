from geosolver.text2.ontology import FunctionNode, function_signatures

__author__ = 'minjoon'

def parse_confident_atoms(graph_parse):
    core_parse = graph_parse.core_parse
    line_graph = graph_parse.line_graph
    circle_dict = graph_parse.circle_dict
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
