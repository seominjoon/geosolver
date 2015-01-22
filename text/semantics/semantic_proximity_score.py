from geosolver.text.semantics.states import SemanticNode

__author__ = 'minjoon'

def semantic_proximity_score(syntax_proximity_score_function, ontology_proximity_score_function, from_node, to_node):
    """
    Combines two score functions (syntax and basic_ontology).
    Can be as simple as the multiplication of the two (which is the case now).

    :param syntax_proximity_score_function:
    :param ontology_proximity_score_function:
    :param from_node:
    :param to_node:
    :return:
    """
    assert isinstance(from_node, SemanticNode)
    assert isinstance(to_node, SemanticNode)

    syntax = from_node.syntax
    basic_ontology = from_node.basic_ontology

    from_token = from_node.token
    to_token = to_node.token
    from_function = from_node.function
    to_function = to_node.function

    syntax_score = syntax_proximity_score_function(syntax, from_token, to_token)
    ontology_score = ontology_proximity_score_function(basic_ontology, from_function, to_function)
    return syntax_score * ontology_score


