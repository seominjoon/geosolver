from collections import namedtuple
from geosolver.ontology.augment_ontology import augment_ontology
from geosolver.text.semantics.ground_token import ground_token
from geosolver.text.semantics.states import SemanticNode

__author__ = 'minjoon'


def create_semantic_nodes(syntax, basic_ontology, ontology_semantics, geowordnet,
                          entry_proximity_score, new_function_identifier, tokens, threshold):
    """
    Returns a tuple (semantic_nodes, new_ontology)
    new ontology is the augmented ontology of new function from semantic nodes.

    :param syntax:
    :param basic_ontology:
    :param ontology_semantics:
    :param geowordnet:
    :param entry_proximity_score:
    :param new_function_identifier:
    :param tokens:
    :param threshold:
    :return:
    """

    semantic_nodes = {}
    new_functions = {}
    token_function_score_pairs = {}
    TokenFunctionScorePair = namedtuple("TokenFunctionScorePair", "token function score")

    for token in tokens:
        function_score_pairs = ground_token(ontology_semantics, geowordnet,
                                            entry_proximity_score, new_function_identifier,
                                            token, threshold)
        for function_name, (function, score) in function_score_pairs.iteritems():
            tfs = TokenFunctionScorePair(token, function, score)
            token_function_score_pairs[(token.index, function.name)] = tfs

            if function_name not in basic_ontology.functions:
                new_functions[function_name] = function

    new_ontology = augment_ontology(basic_ontology, new_functions)

    for token, function, score in token_function_score_pairs.values():
        semantic_node = SemanticNode(syntax, new_ontology, token, function, score)
        semantic_nodes[semantic_node.name] = semantic_node

    return semantic_nodes