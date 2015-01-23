import networkx as nx
import itertools
from geosolver.text.semantics.states import SemanticForest, SemanticNode

__author__ = 'minjoon'


def create_semantic_forest(semantic_nodes, syntax_score_function, ontology_score_function, semantic_score_function):
    assert isinstance(semantic_nodes, dict)

    any_node = semantic_nodes.values()[0]
    assert isinstance(any_node, SemanticNode)

    syntax = any_node.syntax
    basic_ontology = any_node.basic_ontology

    forest_graph = nx.MultiDiGraph()
    edge_scores = {}
    for from_node, to_node in itertools.permutations(semantic_nodes.values(), 2):
        for arg_idx in range(from_node.function.valence):
            syntax_score = modified_syntax_score_function()
            if score > 0:
                edge_scores[(from_node.name, to_node.name)] = score

                if from_node.name not in forest_graph:
                    forest_graph.add_node(from_node.name, label=from_node.label)
                if to_node.name not in forest_graph:
                    forest_graph.add_node(to_node.name, label=to_node.label)

                label = "%d:%.2f" % (arg_idx, score)
                forest_graph.add_edge(from_node.name, to_node.name,
                                      key=arg_idx, arg_idx=arg_idx, score=score, label=label)

    semantic_forest = SemanticForest(syntax, basic_ontology, semantic_nodes, edge_scores, forest_graph)
    return semantic_forest

