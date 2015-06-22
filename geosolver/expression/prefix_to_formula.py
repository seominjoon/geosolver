from geosolver.text2.ontology import FunctionNode, VariableSignature, abbreviations, function_signatures

__author__ = 'minjoon'

def prefix_to_formula(prefix):
    """

    :param list prefix:
    :return FunctionNode:
    """
    if isinstance(prefix, str):
        try:
            return float(prefix)
        except:
            return FunctionNode(VariableSignature(prefix, 'root'), [])
    else:
        return FunctionNode(function_signatures[abbreviations[prefix[0]]],
                            [prefix_to_formula(child) for child in prefix[1:]])
