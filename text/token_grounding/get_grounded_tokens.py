import itertools
from geosolver.geowordnet.identify_constants import identify_constants
from geosolver.geowordnet.filter_functions import filter_functions
from geosolver.text.token_grounding.states import GroundedToken

__author__ = 'minjoon'


def get_grounded_tokens(syntax, ontology_semantics, geowordnet, threshold):
    tokens = {}
    basic_ontology = geowordnet.basic_ontology

    for token in syntax.tokens.values():
        function_score_pairs = filter_functions(ontology_semantics, geowordnet, token.word, threshold)
        constant_score_pairs = identify_constants(basic_ontology, ontology_semantics, token.word)
        for obj, score in itertools.chain(function_score_pairs.itervalues(), constant_score_pairs.itervalues()):
            grounded_token = GroundedToken(syntax, geowordnet.basic_ontology, token, obj, score)
            tokens[grounded_token.key] = grounded_token

    return tokens

