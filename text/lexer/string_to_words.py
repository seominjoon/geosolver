import re

__author__ = 'minjoon'

def string_to_words(string):
    """
    Returns a dictionary of tokens

    :param str string:
    :return dict:
    """
    raw_words = re.split('(\W)', string)
    p = re.compile('\S')
    words = tuple(word for word in raw_words if p.match(word))
    return words
