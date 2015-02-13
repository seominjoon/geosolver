from geosolver.text.lexer.states import Token
from geosolver.text.token_grounding.states import GroundedToken

__author__ = 'minjoon'


def get_grounded_syntax_edge_cost(from_token, to_token, data):
    if isinstance(from_token, GroundedToken) and isinstance(to_token, GroundedToken):
        basic_ontology = from_token.basic_ontology
        entity = basic_ontology.types['entity']
        reference = basic_ontology.types['reference']
        if from_token.ground.type == reference and basic_ontology.isinstance(to_token.ground.type, entity):
            return 0
        elif to_token.ground.type == reference and basic_ontology.isinstance(from_token.ground.type, entity):
            return 0
        else:
            return 1
    else:
        return 1