import networkx as nx
import itertools
from geosolver.text.lexer.states import AbstractToken
from geosolver.text.semantics.states import SemanticForest, SemanticNode

__author__ = 'minjoon'


def create_semantic_forest(semantic_nodes, syntax_score_function, ontology_score_function, semantic_score_function):
    assert isinstance(semantic_nodes, dict)

    any_node = semantic_nodes.values()[0]
    assert isinstance(any_node, SemanticNode)

    syntax = any_node.syntax
    basic_ontology = any_node.basic_ontology


    """
    Create "ground" node and add it to semantic_nodes (creating new dictionary)
    This kind of node is directly
    """
    ground_function = basic_ontology.functions['ground']
    ground_token = AbstractToken('ground')
    ground_node = SemanticNode(syntax, basic_ontology, ground_token, ground_function, 1)
    # Augmentation
    semantic_nodes = dict(semantic_nodes.items() + [(ground_function.name, ground_node)])

    forest_graph = nx.DiGraph()
    edge_scores = {}
    score_function = lambda fn, tn: semantic_score_function(syntax_score_function, ontology_score_function, fn, tn)

    for from_node, to_node in itertools.permutations(semantic_nodes.values(), 2):
        score = score_function(from_node, to_node)
        if score > 0:
            edge_scores[(from_node.name, to_node.name)] = score

            if from_node.name not in forest_graph:
                forest_graph.add_node(from_node.name, label=from_node.label)
            if to_node.name not in forest_graph:
                forest_graph.add_node(to_node.name, label=to_node.label)

            forest_graph.add_edge(from_node.name, to_node.name, label="%.2f" % score, score=score)

    semantic_forest = SemanticForest(syntax, basic_ontology, semantic_nodes, edge_scores, forest_graph)
    return semantic_forest

