from geosolver.utils.prep import display_graph

__author__ = 'minjoon'


class SemanticForest(object):
    def __init__(self, grounded_syntax, graph_nodes, forest_graph):
        self.grounded_syntax = grounded_syntax
        self.forest_graph = forest_graph
        self.basic_ontology = grounded_syntax.basic_ontology
        self.grounded_tokens = grounded_syntax.grounded_tokens
        self.graph_nodes = graph_nodes

    def display_graph(self):
        display_graph(self.forest_graph)


class SemanticRelation(object):
    def __init__(self, from_grounded_token, to_grounded_token,
                 arg_idx, grounded_syntax_path, ontology_path):
        self.from_grounded_token = from_grounded_token
        self.to_grounded_token = to_grounded_token
        self.arg_idx = arg_idx
        self.grounded_syntax_path = grounded_syntax_path
        self.grounded_syntax = grounded_syntax_path.grounded_syntax
        self.ontology_path = ontology_path
        self.basic_ontology = from_grounded_token.basic_ontology
        self.key = (arg_idx, ontology_path.key)
        self.id = (from_grounded_token.key, to_grounded_token.key) + self.key

    def __repr__(self):
        return "%s(%r, %r)" % (self.__class__.__name__, self.grounded_syntax_path, self.ontology_path)


class TypeRelation(object):
    def __init__(self, from_type, to_grounded_token, ontology_path):
        self.from_type = from_type
        self.to_grounded_token = to_grounded_token
        self.ontology_path = ontology_path
        self.key = ontology_path.key
        self.id = (from_type.name, to_grounded_token.key, self.key)
        self.basic_ontology = to_grounded_token.basic_ontology


class SemanticTree(object):
    def __init__(self, semantic_forest, tree_graph, formula):
        assert isinstance(semantic_forest, SemanticForest)
        self.semantic_forest = semantic_forest
        self.grounded_syntax = semantic_forest.grounded_syntax
        self.basic_ontology = semantic_forest.basic_ontology
        self.tree_graph = tree_graph
        self.formula = formula
        self.return_type = formula.current.return_type

    def display_graph(self):
        display_graph(self.tree_graph)

"""
class SemanticWeight(object):
    def __init__(self, semantic_forest, node_weights, edge_weights):
        assert isinstance(semantic_forest, SemanticForest)
        assert isinstance(node_weights, dict)
        assert isinstance(edge_weights, dict)
        self.semantic_forest = semantic_forest
        self.node_weights = node_weights
        self.edge_weights = edge_weights
"""


class ImpliedInstance(object):
    def __init__(self, grounded_syntax, parent_grounded_token, arg_idx, ground):
        self.grounded_syntax = grounded_syntax
        self.parent_grounded_token = parent_grounded_token
        self.arg_idx = arg_idx
        self.ground = ground
        self.key = (parent_grounded_token.key, arg_idx)
        self.label = ground.label


class ImpliedSourceFunction(object):
    def __init__(self, grounded_syntax, function, child_grounded_tokens):
        self.grounded_syntax = grounded_syntax
        self.basic_ontology = grounded_syntax.basic_ontology
        self.ground = function
        self.child_grounded_tokens = child_grounded_tokens
        self.key = (function.key, ) + tuple(t.key for t in child_grounded_tokens)
        self.label = "implied_%s" % function.name