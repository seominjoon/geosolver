from geosolver.text.lexer.states import Token
import re

__author__ = 'minjoon'


def string_to_tokens(string):
    """
    Returns a dictionary of tokens

    :param str string:
    :return dict:
    """
    raw_words = re.split('(\W)', string)
    p = re.compile('\S')
    words = tuple(word for word in raw_words if p.match(word))
    sentence = {idx: word for idx, word in enumerate(words)}
    tokens = {idx: Token(sentence, idx) for idx in sentence}
    return tokens


def sentence_to_tokens(sentence):
    tokens = {idx: Token(sentence, idx) for idx in sentence}
    return tokens

