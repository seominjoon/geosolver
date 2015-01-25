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
        self.id = type_.name
        self.label = type_.name

    def __repr__(self):
        return "%s(type=%s)" % (self.__class__.__name__, self.type.name)


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
        self.id = (token.index, function.name)
        self.syntax = syntax
        self.basic_ontology = basic_ontology
        self.score = score

    def __repr__(self):
        return "%s(%r, %r)" % (self.__class__.__name__, self.token, self.function)


class SemanticForest(object):
    def __init__(self, syntax, basic_ontology, source_nodes, semantic_nodes, forest_graph):
        assert isinstance(syntax, Syntax)
        assert isinstance(basic_ontology, BasicOntology)
        assert isinstance(forest_graph, nx.DiGraph)
        assert isinstance(semantic_nodes, dict)
        for node in semantic_nodes.values():
            assert isinstance(node, SemanticNode)

        self.syntax = syntax
        self.basic_ontology = basic_ontology
        self.source_nodes = source_nodes
        self.semantic_nodes = semantic_nodes
        self.forest_graph = forest_graph

    def display_graph(self):
        """
        Display the forest graph
        Edges will be labeled with scores.
        :return:
        """
        display_graph(self.forest_graph)


class Relation(object):
    pass

class SemanticRelation(Relation):
    def __init__(self, from_semantic_node, to_semantic_node, arg_idx, syntax_path, ontology_path):
        self.from_semantic_node = from_semantic_node
        self.to_semantic_node = to_semantic_node
        self.arg_idx = arg_idx
        self.key = (arg_idx, syntax_path.tree_rank, ontology_path.key)
        self.id = (arg_idx, syntax_path.id, ontology_path.id)
        self.syntax_path = syntax_path
        self.ontology_path = ontology_path
        self.syntax = syntax_path.syntax
        self.basic_ontology = ontology_path.basic_ontology


class SourceRelation(Relation):
    def __init__(self, source_node, semantic_node, ontology_path):
        self.from_source_node = source_node
        self.to_semantic_node = semantic_node
        self.ontology_path = ontology_path
        self.key = ontology_path.key
        self.id = ontology_path.id

