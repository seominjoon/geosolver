from collections import namedtuple
from geosolver.geowordnet.filter_functions import filter_functions
from geosolver.ontology.augment_ontology import augment_ontology
from geosolver.text.grounding.states import GroundedToken

__author__ = 'minjoon'


def get_grounded_tokens(syntax, ontology_semantics, geowordnet, threshold):
    tokens = {}
    basic_ontology = geowordnet.basic_ontology
    new_functions = {}
    token_function_score_pairs = {}

    TokenFunctionScorePair = namedtuple("TokenFunctionScorePair", "token function score")

    for token in syntax.tokens.values():
        function_score_pairs = filter_functions(ontology_semantics, geowordnet, token.word, threshold)
        for function, score in function_score_pairs.values():
            if function.name not in basic_ontology.functions:
                new_functions[function.name] = function
            token_function_score_pairs[(token.index, function.name)] = TokenFunctionScorePair(token, function, score)

    new_ontology = augment_ontology(basic_ontology, new_functions)
    for token, function, score in token_function_score_pairs.values():
        grounded_token = GroundedToken(syntax, new_ontology, token, function, score)
        tokens[grounded_token.key] = grounded_token

    return tokens

