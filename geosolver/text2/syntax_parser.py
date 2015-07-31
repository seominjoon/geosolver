__author__ = 'minjoon'

class SyntaxParse(object):
    def __init__(self, words, graph):
        self.words = words
        self.graph = graph

    def get_words(self, span):
        return tuple(self.words[idx] for idx in range(*span))

    def iterate_spans(self, maxlen=2):
        for start in range(len(self.words)):
            for spanlen in range(maxlen):
                end = start + spanlen
                if end <= len(self.words):
                    yield (start, end)
