from collections import namedtuple
from geosolver.geowordnet.filter_functions import filter_functions
from geosolver.ontology.augment_ontology import augment_ontology
from geosolver.text.semantics.ground_token import ground_token
from geosolver.text.semantics.states import SemanticNode

__author__ = 'minjoon'


def create_semantic_nodes(syntax, basic_ontology, ontology_semantics, geowordnet, tokens, threshold):
    semantic_nodes = {}
    new_functions = {}
    token_function_score_pairs = {}

    TokenFunctionScorePair = namedtuple("TokenFunctionScorePair", "token function score")

    for token in tokens.values():
        function_score_pairs = ground_token(ontology_semantics, geowordnet, filter_functions, token, threshold)
        for function, score in function_score_pairs.values():
            tfs = TokenFunctionScorePair(token, function, score)
            token_function_score_pairs[(token.index, function.name)] = tfs

            if function.name not in basic_ontology.functions:
                new_functions[function.name] = function

    new_ontology = augment_ontology(basic_ontology, new_functions)

    for token, function, score in token_function_score_pairs.values():
        semantic_node = SemanticNode(syntax, new_ontology, token, function, score)
        semantic_nodes[semantic_node.id] = semantic_node

    return semantic_nodes