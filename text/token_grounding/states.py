from geosolver.text.lexer.states import Token
from geosolver.text.syntax.states import SyntaxTree, Syntax, SyntaxPath
from geosolver.utils import display_graph, display_graphs

__author__ = 'minjoon'


class GroundedToken(Token):
    def __init__(self, syntax, basic_ontology, token, function, score):
        self.syntax = syntax
        self.basic_ontology = basic_ontology
        self.token = token
        self.function = function
        self.score = score
        self.key = (token.index, function.name)
        self.index = token.index
        self.name = function.name
        self.label = "%d, %s" % self.key
        self.sentence = token.sentence
        self.word = token.word

    def __repr__(self):
        return "%s(index=%d, name=%s)" % (self.__class__.__name__, self.index, self.name)


class GroundedSyntaxTree(object):
    def __init__(self, grounded_tokens, graph, rank, score):
        self.grounded_tokens = grounded_tokens
        self.graph = graph
        self.rank = rank
        self.score = score

    def display_graph(self):
        display_graph(self.graph)


class GroundedSyntax(Syntax):
    def __init__(self, syntax, basic_ontology, grounded_tokens, grounded_syntax_trees):
        self.syntax = syntax
        self.basic_ontology = basic_ontology
        self.tokens = syntax.tokens
        self.syntax_trees = syntax.syntax_trees
        self.grounded_tokens = grounded_tokens
        self.grounded_syntax_trees = grounded_syntax_trees
        self.all_tokens = dict(self.tokens.items() + self.grounded_tokens.items())

    def display_graphs(self):
        display_graphs(grounded_syntax_tree.graph for grounded_syntax_tree in self.grounded_syntax_trees.values())


class GroundedSyntaxPath(SyntaxPath):
    def __init__(self, grounded_syntax, tree_rank, tokens, cost):
        self.grounded_syntax = grounded_syntax
        self.syntax = grounded_syntax.syntax
        self.tree_rank = tree_rank
        self.tokens = tokens
        self.cost = cost
        self.id = (tokens[0].key, tokens[-1].key, tree_rank)
        self.basic_ontology = grounded_syntax.basic_ontology

