import itertools
from geosolver.ontology.ontology_definitions import FormulaNode, signatures, FunctionSignature

__author__ = 'minjoon'

def parse_confident_formulas(graph_parse):
    eps = 0.5 # to be updated by the scale of the diagram
    core_parse = graph_parse.core_parse
    line_graph = graph_parse.line_graph
    circle_dict = graph_parse.circle_dict
    confident_formulas = []

    for from_key, to_key, data in line_graph.edges(data=True):
        line_variable = FormulaNode(signatures['Line'],
                                     [core_parse.point_variables[from_key], core_parse.point_variables[to_key]])
        points = data['points']
        for point_key, point in points.iteritems():
            point_variable = core_parse.point_variables[point_key]
            variable_node = FormulaNode(signatures['PointLiesOnLine'], [point_variable, line_variable])
            confident_formulas.append(variable_node)

    for center_key, d in circle_dict.iteritems():
        for radius_key, dd in d.iteritems():
            circle_variable = FormulaNode(signatures['Circle'],
                                           [core_parse.point_variables[center_key],
                                            core_parse.radius_variables[center_key][radius_key]])
            points = dd['points']
            for point_key, point in points.iteritems():
                point_variable = core_parse.point_variables[point_key]
                variable_node = FormulaNode(signatures['PointLiesOnCircle'], [point_variable, circle_variable])
                confident_formulas.append(variable_node)

    # Just enforce non collapsing between known labels?
    """
    for from_point, to_point in itertools.combinations(graph_parse.core_parse.point_variables.values(), 2):
        line = FormulaNode(signatures['Line'], [from_point, to_point])
        length = FormulaNode(signatures['SquaredLengthOf'], [line])
        threshold = FormulaNode(FunctionSignature(str(eps**2), 'number', []), [])
        formula = FormulaNode(signatures['Ge'], [length, threshold])
        confident_formulas.append(formula)
    """

    return confident_formulas
