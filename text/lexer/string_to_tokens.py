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
    sentence = tuple(word for word in raw_words if p.match(word))
    tokens = tuple(Token(sentence, idx) for idx in range(len(sentence)))
    return tokens
