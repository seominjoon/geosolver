from geosolver.geowordnet import geowordnet
from geosolver.geowordnet.filter_functions import filter_functions
from geosolver.ontology import ontology_semantics
from geosolver.text.lexer.states import Token, ExpressionParse
from geosolver.text.lexer.string_to_words import string_to_words

__author__ = 'minjoon'


dummy_sentence = "a statement is true".split(' ')
k = 1
dummy_noun = "a value".split(' ')
operators = "+-*/=><^:"
comparators = "=><"

def separate_expressions(sentence):
    """

    :param tokens:
    :return:
    """
    temp_words = []
    equations = []
    current_equation = []
    flags = [is_operator(word) for word in sentence.values()]
    neighbor_flags = [is_neighbor(sentence.values(), flags, idx) for idx in sentence]
    extended_flags = [is_extended(sentence.values(), neighbor_flags, idx) for idx in sentence]

    previous_flag = False
    for idx, word in sentence.iteritems():
        if previous_flag and not extended_flags[idx]:
            """
            Exited equation.
            """
            expression = ExpressionParse(current_equation, len(temp_words)+k)
            equations.append(expression)
            if has_comparator(current_equation):
                temp_words.extend(dummy_sentence)
            else:
                temp_words.extend(dummy_noun)
            current_equation = []
        if extended_flags[idx]:
            current_equation.append(word)
        else:
            temp_words.append(word)
        previous_flag = extended_flags[idx]
    if len(current_equation) > 0:
        equations.append(current_equation)

    return _words_to_tokens(temp_words), equations

def _words_to_tokens(words):
    sentence = {idx: word for idx, word in enumerate(words)}
    return {idx: Token(sentence, idx) for idx, word in enumerate(words)}


def is_operator(word):
    if word in operators:
        return True
    return False


def has_comparator(words):
    for comparator in comparators:
        if comparator in words:
            return True
    return False


def is_neighbor(words, flags, idx):
    if flags[idx]:
        return True
    if idx > 0:
        if flags[idx-1]:
            return True
    if idx < len(words) -1:
        if flags[idx+1]:
            return True
    return False


def is_extended(words, flags, idx):
    if flags[idx]:
        return True
    if idx < len(words) - 1:
        if flags[idx+1] and len(filter_functions(ontology_semantics, geowordnet, words[idx], 0.99)) > 0:
            return True
    return False