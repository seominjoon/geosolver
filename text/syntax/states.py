from collections import namedtuple
from geosolver.text.syntax.misc import syntax_display_graphs
from geosolver.text.syntax.syntax_proximity_score import syntax_proximity_score

__author__ = 'minjoon'


class Syntax(object):
    def __init__(self, tokens, syntax_graph_score_pairs):
        self.tokens = tokens
        self.syntax_graph_score_pairs = syntax_graph_score_pairs
        self.sentence = tokens[0].sentence

    def display_graphs(self):
        """
        Displays all syntax graphs.
        Used for debugging

        :return:
        """
        syntax_display_graphs(self)

    def proximity_score(self, from_token, to_token):
        return syntax_proximity_score(self, from_token, to_token)

TreeScorePair = namedtuple("TreeScorePair", "tree score")
