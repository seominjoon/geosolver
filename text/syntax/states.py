__author__ = 'minjoon'


class Token(object):
    def __init__(self, sentence, index):
        self.sentence = sentence
        self.index = index
        self.word = sentence[index]


class Syntax(object):
    def __init__(self, tokens, syntax_graph_score_pairs):
        self.tokens = tokens
        self.syntax_graph_score_pairs = syntax_graph_score_pairs
        self.sentence = tokens[0].sentence