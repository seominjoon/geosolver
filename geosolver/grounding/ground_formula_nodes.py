from geosolver.grounding.states import MatchParse
from geosolver.text2.ontology import VariableSignature, function_signatures, FormulaNode, SetNode

__author__ = 'minjoon'

def ground_formula_nodes(match_parse, formula_nodes):
    """
    Based on the match parse, return the grounded function node.
    That is, every variable in the function node is replaced with a variable in match_parse
    For now, assume this is deterministic (i.e. variable type is not entity)

    :param match_parse:
    :param function_node:
    :return:
    """
    return [_ground_formula_node(match_parse, formula_node) for formula_node in formula_nodes]

def _ground_formula_node(match_parse, formula_node):
    if not isinstance(formula_node, FormulaNode) and not isinstance(formula_node, SetNode):
        return formula_node
    elif isinstance(formula_node, FormulaNode) and formula_node.is_leaf():
        if formula_node.signature.id in function_signatures:
            return formula_node
        return _ground_leaf(match_parse, formula_node, formula_node.return_type)
    elif isinstance(formula_node, FormulaNode):
        children = [_ground_formula_node(match_parse, child) for child in formula_node.children]
        return FormulaNode(formula_node.signature, children)
    elif isinstance(formula_node, SetNode):
        members = [_ground_formula_node(match_parse, member) for member in formula_node.children]
        return SetNode(members)


def _infer_return_type(match_parse, atoms, variable_signature):
    pass



def _ground_leaf(match_parse, leaf, return_type):
    assert isinstance(leaf, FormulaNode)
    assert isinstance(match_parse, MatchParse)
    variable_signature = leaf.signature
    if return_type == 'number':
        if len(variable_signature.name) == 1:
            return FormulaNode(variable_signature, [])
        elif len(variable_signature.name) == 2:
            return FormulaNode(function_signatures['LengthOf'], [_ground_leaf(match_parse, leaf, 'line')])
    elif return_type == 'point':
        return match_parse.match_dict[variable_signature.name][0]
    elif return_type == 'line':
        if len(variable_signature.name) == 1:
            line = match_parse.match_dict[variable_signature.name][0]
            return line
        elif len(variable_signature.name) == 2:
            label_a, label_b = variable_signature.name
            point_a = match_parse.match_dict[label_a][0]
            point_b = match_parse.match_dict[label_b][0]
            return FormulaNode(function_signatures['Line'], [point_a, point_b])
    elif return_type == 'circle':
        assert len(variable_signature.name) == 1
        center_label = variable_signature.name
        center = match_parse.match_dict[center_label][0]
        center_idx = int(center.signature.name.split("_")[1])
        radius = match_parse.graph_parse.core_parse.radius_variables[center_idx][0]
        return FormulaNode(function_signatures['Circle'], [center, radius])
    elif return_type == 'angle':
        # TODO :
        if len(variable_signature.name) == 3:
            label_a, label_b, label_c = variable_signature.name
            point_a = match_parse.match_dict[label_a][0]
            point_b = match_parse.match_dict[label_b][0]
            point_c = match_parse.match_dict[label_c][0]
            return FormulaNode(function_signatures['Angle'], [point_a, point_b, point_c])
        else:
            raise Exception()
    elif return_type == 'triangle':
        if len(variable_signature.name) == 3:
            label_a, label_b, label_c = variable_signature.name
            point_a = match_parse.match_dict[label_a][0]
            point_b = match_parse.match_dict[label_b][0]
            point_c = match_parse.match_dict[label_c][0]
            return FormulaNode(function_signatures['Triangle'], [point_a, point_b, point_c])
        else:
            raise Exception()
    elif return_type == 'quad':
        pass

    raise Exception()

