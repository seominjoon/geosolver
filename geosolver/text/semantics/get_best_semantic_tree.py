from collections import namedtuple
from geosolver.text.semantics.costs.get_semantic_tree_graph_cost import get_semantic_tree_graph_cost
from geosolver.text.semantics.states import SemanticForest, SemanticWeight, SemanticTree
from geosolver.text.semantics.tree_graph_to_formula import tree_graph_to_formula
from geosolver.text.token_grounding.states import GroundedToken
import networkx as nx

__author__ = 'minjoon'

GraphCostPair = namedtuple("GraphCostPair", "graph cost")
GraphHeadKeyCostPair = namedtuple("KeyGraphCostPair", "graph head key cost")

def get_best_semantic_tree(semantic_forest, head_type, semantic_weight):
    head_type_key = head_type.id
    semantic_trees = []
    for u, v in semantic_forest.forest_graph.edges(head_type_key):
        pair = _get_best_graph_cost_pair(semantic_forest, v, semantic_weight)
        assert isinstance(pair, GraphCostPair)

        formula = tree_graph_to_formula(semantic_forest, pair.graph, v)
        semantic_tree = SemanticTree(semantic_forest, pair.graph, pair.cost, formula)
        semantic_trees.append(semantic_tree)
    return min(semantic_trees, key=lambda tree: tree.cost)

def _get_best_graph_cost_pair(semantic_forest, head_key, semantic_weight):
    assert isinstance(semantic_forest, SemanticForest)
    assert isinstance(semantic_weight, SemanticWeight)
    basic_ontology = semantic_forest.basic_ontology
    obj = semantic_forest.graph_nodes[head_key]

    if isinstance(obj, GroundedToken):
        function = obj.function
    else:
        raise Exception

    graph = nx.MultiDiGraph()
    graph.add_node(head_key)
    if function.valence == 0:
        cost = get_semantic_tree_graph_cost(semantic_forest, graph, semantic_weight)
        return GraphCostPair(graph, cost)

    else:
        all_pairs = [[] for _ in range(function.valence)]
        for u, v, edge_key, data in semantic_forest.forest_graph.edges(keys=True, data=True):
            v_graph, v_cost = _get_best_graph_cost_pair(semantic_forest, v, semantic_weight)
            arg_idx = data['arg_idx']
            pair = GraphHeadKeyCostPair(v_graph, v, edge_key, v_cost)
            all_pairs[arg_idx].append(pair)

        for arg_idx, pairs in enumerate(all_pairs):
            best_pair = min(pairs, key=lambda p: _get_cost(semantic_forest, head_key, p, semantic_weight))
            graph = nx.union(graph, best_pair.graph)
            graph.add_edge(head_key, best_pair.head, arg_idx=arg_idx, key=best_pair.key)

        cost = get_semantic_tree_graph_cost(semantic_forest, graph, semantic_weight)
        return GraphCostPair(graph, cost)

def _get_cost(semantic_forest, u, ghkcp, semantic_weight):
    new_graph = ghkcp.graph.copy()
    new_graph.add_edge(u, ghkcp.head, key=ghkcp.key)
    return get_semantic_tree_graph_cost(semantic_forest, new_graph, semantic_weight)
