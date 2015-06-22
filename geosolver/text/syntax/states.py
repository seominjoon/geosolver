from geosolver.text.syntax.misc import syntax_display_graphs, syntax_save_graphs
from geosolver.utils.prep import display_graph

__author__ = 'minjoon'


class Syntax(object):
    def __init__(self, tokens, syntax_trees):
        assert isinstance(tokens, dict)
        assert isinstance(syntax_trees, dict)
        self.tokens = tokens
        self.syntax_trees = syntax_trees
        self.sentence = tokens[0].sentence

    def display_graphs(self):
        """
        Displays all syntax graphs.
        Used for debugging

        :return:
        """
        syntax_display_graphs(self)

    def save_graphs(self, root_path):
        syntax_save_graphs(self, root_path)


class SyntaxTree(object):
    def __init__(self, graph, rank, score):
        self.graph = graph
        self.rank = rank
        self.score = score

    def display_graph(self):
        display_graph(self.graph)

    def __repr__(self):
        return "%s(rank=%d, score=%.2f)" % (self.__class__.__name__, self.rank, self.score)


class SyntaxPath(object):
    def __init__(self, syntax, tree_rank, tokens):
        self.syntax = syntax
        self.tree_rank = tree_rank
        self.tokens = tokens
        self.id = (tokens[0].index, tokens[-1].index, tree_rank)

    def __len__(self):
        return len(self.tokens)

    def __repr__(self):
        return "%s(rank=%d, tokens=[%s])" % (self.__class__.__name__,
                                             self.tree_rank, ', '.join(token.word for token in self.tokens))

