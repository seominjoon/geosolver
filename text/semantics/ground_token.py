from geosolver.geowordnet.filter_functions import filter_functions
from geosolver.text.lexer.states import Token

__author__ = 'minjoon'

def ground_token(ontology_semantics, geowordnet, filter_functions, token, threshold):
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

    return filter_functions(ontology_semantics, geowordnet, token.word, threshold)

