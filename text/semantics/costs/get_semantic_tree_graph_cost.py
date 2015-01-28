from geosolver.text.semantics.states import SemanticForest, SemanticWeight
import networkx as nx

__author__ = 'minjoon'

def get_semantic_tree_graph_cost(semantic_forest, graph, semantic_weight):
    assert isinstance(semantic_forest, SemanticForest)
    assert isinstance(graph, nx.MultiDiGraph)
    assert isinstance(semantic_weight, SemanticWeight)

    o = 2.0
    s = 1.0
    w = 0.1

    ontology_cost = 0
    syntax_cost = 0
    weight = 0
    for node_key in graph.nodes():
        weight += semantic_weight.node_weights[node_key]

    for u, v, key in graph.edges(keys=True):
        ontology_cost += semantic_forest.forest_graph[u][v][key]['ontology_cost']
        syntax_cost += semantic_forest.forest_graph[u][v][key]['syntax_cost']
        weight += semantic_weight.edge_weights[(u, v, key)]

    return o*ontology_cost + s*syntax_cost + w*weight