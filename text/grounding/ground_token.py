from geosolver.text.grounding.states import GroundedToken
from geosolver.text.lexer.states import Token

__author__ = 'minjoon'

def ground_token(syntax, ontology_semantics, geowordnet, filter_functions, token, threshold):
    """
    Given token, find the best matching function score function.
    Score function takes in word and threshold.
    Usually, entry_score_function is geowordnet.
    It filters all functions whose proximity score is higher than the threshold.
    Returns a dictionary where key is the function's name, and the value is FuncionScorePair(function, score)

    :param entry_score_function:
    :param Token token:
    :param float threshold:
    :return dict:
    """
    assert isinstance(token, Token)
    basic_ontology = geowordnet.basic_ontology

    function_score_pairs = filter_functions(ontology_semantics, geowordnet, token.word, threshold)
    assert isinstance(function_score_pairs, dict)

    grounded_tokens = {}
    for function, score in function_score_pairs.values():
        grounded_token = GroundedToken(syntax, basic_ontology, token, function, score)
        grounded_tokens[grounded_token.key] = grounded_token

    # Add itself
    grounded_tokens[token.key] = token
    return grounded_tokens


