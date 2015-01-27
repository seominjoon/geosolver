from collections import namedtuple
import itertools
import networkx as nx
from geosolver.ontology.states import Type
from geosolver.text.semantics.states import SemanticTree
from geosolver.text.token_grounding.states import GroundedToken

__author__ = 'minjoon'

GraphHeadCostPair = namedtuple("GraphScorePair", "graph head syntax_cost ontology_cost")


def get_semantic_trees(semantic_forest, head):
    assert isinstance(head, Type)
    head_key = head.id
    nodes = _get_nodes(semantic_forest, head_key)
    trees = [_node_to_tree(semantic_forest, node) for node in nodes]
    sorted_trees = sorted(trees, key=lambda tree: tree.ontology_cost + tree.grounded_syntax_cost)
    tree_dict = {idx: tree for idx, tree in enumerate(sorted_trees)}
    return tree_dict


def _get_nodes(semantic_forest, head_key):
    head = semantic_forest.graph_nodes[head_key]
    if isinstance(head, GroundedToken) and head.function.valence == 0:
        node = Node(head_key, [], [], [])
        return [node]
    else:
        if isinstance(head, Type):
            nodes = []
            for u, v, data in semantic_forest.forest_graph.edges(head_key, data=True):
                children_nodes = _get_nodes(semantic_forest, v)
                edge_syntax_cost = data['syntax_cost']
                edge_ontology_cost = data['ontology_cost']
                for child_node in children_nodes:
                    new_node = Node(head_key, [child_node], [edge_syntax_cost], [edge_ontology_cost])
                    nodes.append(new_node)
            return nodes
        elif isinstance(head, GroundedToken):
            children_list = [[] for idx in range(head.function.valence)]
            for u, v, data in semantic_forest.forest_graph.edges(head_key, data=True):
                edge_syntax_cost = data['syntax_cost']
                edge_ontology_cost = data['ontology_cost']
                arg_idx = data['arg_idx']
                new_nodes = _get_nodes(semantic_forest, v)
                new_pairs = [[new_node, edge_syntax_cost, edge_ontology_cost] for new_node in new_nodes]
                children_list[arg_idx].extend(new_pairs)

            nodes = []
            for pairs in itertools.product(*children_list):
                arg_nodes, syntax_costs, ontology_costs = zip(*pairs)
                new_node = Node(head_key, arg_nodes, syntax_costs, ontology_costs)
                nodes.append(new_node)
            return nodes
        else:
            raise Exception()


def _node_to_tree(semantic_forest, node):
    graph = nx.MultiDiGraph()
    _fill_graph(semantic_forest, graph, node)
    ontology_cost = 0
    syntax_cost = 0
    for u, v, data in graph.edges(data=True):
        ontology_cost += data['ontology_cost']
        syntax_cost += data['syntax_cost']
    tree = SemanticTree(semantic_forest, graph, syntax_cost, ontology_cost)
    return tree

def _fill_graph(semantic_forest, graph, node):
    head = semantic_forest.graph_nodes[node.head_key]
    graph.add_node(node.head_key, label=head.label)
    for idx, child in enumerate(node.children):
        _fill_graph(semantic_forest, graph, child)
        sc = node.syntax_scores[idx]
        oc = node.ontology_scores[idx]
        graph.add_edge(node.head_key, child.head_key, label="%.1f, %.1f" % (sc, oc),
                       syntax_cost=sc, ontology_cost=oc, key=idx)


class Node(object):
    def __init__(self, head_key, children, syntax_scores, ontology_scores):
        self.head_key = head_key
        self.children = children
        self.syntax_scores = syntax_scores
        self.ontology_scores = ontology_scores
