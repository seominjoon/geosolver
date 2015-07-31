__author__ = 'minjoon'

class SyntaxParse(object):
    def __init__(self, words, graph):
        self.words = words
        self.graph = graph

    def get_words(self, span):
        return tuple(self.words[idx] for idx in range(*span))