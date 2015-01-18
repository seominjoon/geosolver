import re

__author__ = 'minjoon'


def string_to_words(string):
    raw_words = re.split('(\W)', string)
    p = re.compile('\S')
    words = [word for word in raw_words if p.match(word)]
    return words
