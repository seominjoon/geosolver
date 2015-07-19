from geosolver.ontology.ontology_definitions import FormulaNode, VariableSignature, abbreviations, signatures, FunctionSignature
from geosolver.utils.num import is_number

__author__ = 'minjoon'

def prefix_to_formula(prefix):
    """

    :param list prefix:
    :return FormulaNode:
    """
    if isinstance(prefix, str):
        if prefix in abbreviations:
            return FormulaNode(signatures[abbreviations[prefix]], [])
        elif is_number(prefix):
            return FormulaNode(FunctionSignature(prefix, 'number', []), [])
        else:
            return FormulaNode(VariableSignature(prefix, 'number'), [])
    else:
        return FormulaNode(signatures[abbreviations[prefix[0]]],
                            [prefix_to_formula(child) for child in prefix[1:]])
