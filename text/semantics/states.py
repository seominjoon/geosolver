from geosolver.ontology.states import Function, BasicOntology, Type
from geosolver.text.lexer.states import Token
from geosolver.text.syntax.states import Syntax
import networkx as nx
from geosolver.utils import display_graph

__author__ = 'minjoon'


class Node(object):
    """
    Must define self.name and self.label
    """
    pass


class SourceNode(Node):
    def __init__(self, type_):
        assert isinstance(type_, Type)
        self.type = type_
        self.name = type_.name
        self.label = type_.name

    def __repr__(self):
        return "%s(type=%s)" % (self.__class__.__name__, self.type.name)


class SinkNode(Node):
    def __init__(self):
        self.name = 'sink'
        self.label = self.name

    def __repr__(self):
        return "%s()" % self.__class__.__name__


class SemanticNode(Node):
    def __init__(self, syntax, basic_ontology, token, function, score):
        """
        Nodes are indexed by their ids in graphs.

        :param syntax:
        :param basic_ontology:
        :param token:
        :param function:
        :param score:
        :return:
        """
        assert isinstance(syntax, Syntax)
        assert isinstance(basic_ontology, BasicOntology)
        assert isinstance(token, Token)
        assert isinstance(function, Function)
        self.token = token
        self.function = function
        self.label = "%s, %s" % (token.label, function.label)
        self.name = (token.name, function.name)
        self.id = hash(self.name)
        self.syntax = syntax
        self.basic_ontology = basic_ontology
        self.score = score

    def __repr__(self):
        return "%s(%r, %r)" % (self.__class__.__name__, self.token, self.function)


class SemanticForest(object):
    def __init__(self, syntax, basic_ontology, nodes, edge_scores, forest_graph):
        assert isinstance(syntax, Syntax)
        assert isinstance(basic_ontology, BasicOntology)
        assert isinstance(forest_graph, nx.DiGraph)
        assert isinstance(nodes, dict)
        for node in nodes.values():
            assert isinstance(node, SemanticNode)

        self.syntax = syntax
        self.basic_ontology = basic_ontology
        self.nodes = nodes
        self.edge_scores = edge_scores
        self.forest_graph = forest_graph

    def display_graph(self):
        """
        Display the forest graph
        Edges will be labeled with scores.
        :return:
        """
        display_graph(self.forest_graph)
