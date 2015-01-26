from geosolver.geowordnet.filter_functions import filter_functions
from geosolver.text.grounding.ground_token import ground_token

__author__ = 'minjoon'

def get_grounded_tokens(syntax, ontology_semantics, geowordnet, threshold):
    token_items = []
    for token in syntax.tokens.values():
        local_tokens = ground_token(syntax, ontology_semantics, geowordnet, filter_functions, token, threshold)
        token_items.extend(local_tokens.items())

    tokens = dict(token_items)
    return tokens

