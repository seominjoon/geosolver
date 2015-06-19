from geosolver.grounding.states import MatchParse
from geosolver.text2.ontology import VariableSignature, function_signatures, FunctionNode

__author__ = 'minjoon'

def ground_atoms(match_parse, atoms):
    """
    Based on the match parse, return the grounded function node.
    That is, every variable in the function node is replaced with a variable in match_parse
    For now, assume this is deterministic (i.e. variable type is not entity)

    :param match_parse:
    :param function_node:
    :return:
    """
    return [_ground_atom(match_parse, atom) for atom in atoms]

def _ground_atom(match_parse, atom):
    if not isinstance(atom, FunctionNode):
        return atom
    elif atom.is_leaf():
        return _ground_leaf(match_parse, atom, atom.return_type)
    else:
        children = [_ground_atom(match_parse, child) for child in atom.children]
        return FunctionNode(atom.signature, children)


def _infer_return_type(match_parse, atoms, variable_signature):
    pass



def _ground_leaf(match_parse, leaf, return_type):
    assert isinstance(leaf, FunctionNode)
    assert isinstance(match_parse, MatchParse)
    variable_signature = leaf.signature
    if return_type == 'number':
        return FunctionNode(variable_signature, [])
    elif return_type == 'point':
        return match_parse.match_dict[variable_signature.id][0]
    elif return_type == 'line':
        assert len(variable_signature.id) == 2
        label_a, label_b = variable_signature.id
        point_a = match_parse.match_dict[label_a][0]
        point_b = match_parse.match_dict[label_b][0]
        return FunctionNode(function_signatures['Line'], [point_a, point_b])
    elif return_type == 'circle':
        assert len(variable_signature.id) == 1
        center_label = variable_signature.id
        center = match_parse.match_dict[center_label][0]
        center_idx = int(center.signature.id.split("_")[1])
        radius = match_parse.graph_parse.core_parse.radius_variables[center_idx][0]
        return FunctionNode(function_signatures['Circle'], [center, radius])
    elif return_type == 'triangle':
        pass
    elif return_type == 'quad':
        pass

