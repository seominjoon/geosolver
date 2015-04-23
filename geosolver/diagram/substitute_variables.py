import sympy
from geosolver.diagram.states import GeneralDiagramParse
from geosolver.ontology.states import Formula, Constant, Function
from geosolver.utils import index_by_list

__author__ = 'minjoon'

def substitute_variables(general_diagram_parse, diagram_formula):
    """
    formula is diagram-grounded with variables.
    Substitute the variables in the formula with values

    :param general_graph_parse:
    :param formula:
    :return:
    """
    assert isinstance(general_diagram_parse, GeneralDiagramParse)
    assert isinstance(diagram_formula, Formula)

    current = diagram_formula.current

    if isinstance(current, Constant):
        """
        Then the formula should not have any child...
        """
        assert len(current.children) == 0
        new_constant = Constant(_evaluate_constant(general_diagram_parse, current.content), current.type)
        return Formula(diagram_formula.basic_ontolgy, new_constant, [])

    elif isinstance(current, Function):
        return Formula(diagram_formula.basic_ontolgy, current,
                           [substitute_variables(general_diagram_parse, child) for child in diagram_formula.children])

    else:
        raise Exception("Something went wrong...")


def _evaluate_constant(general_diagram_parse, content):
    """

    :param general_graph_parse:
    :param variable:
    :return:
    """
    if isinstance(content, sympy.Symbol):
        return _get_value(general_diagram_parse, content)
    else:
        args = [_evaluate_constant(general_diagram_parse, child) for child in content]
        return type(content)(*args)


def _get_value(general_diagram_parse, variable):
    """
    Find variable in general_diagram_parse.variables
    Find the corresponding value.
    Return the value


    :param general_diagram_parse:
    :param variable: sympy symbol; separate by underscore to get ('points', 5, 'x'), ('radii', 3, 2), etc.
    :return:
    """
    assert isinstance(variable, sympy.Symbol)
    indices = str(variable).split("_")
    if indices[0] == 'points':
        indices[1] = int(indices[1])
    elif indices[0] == 'radii':
        indices[1] = int(indices[1])
        indices[2] = int(indices[2])

    return index_by_list(general_diagram_parse.values, indices)