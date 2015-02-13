from collections import namedtuple
import itertools
import networkx as nx
from geosolver.ontology.states import Type, Constant
from geosolver.text.semantics.states import SemanticTree, ImpliedInstance, ImpliedSourceFunction
from geosolver.text.semantics.tree_graph_to_formula import tree_graph_to_formula
from geosolver.text.token_grounding.states import GroundedToken

__author__ = 'minjoon'

GraphHeadCostPair = namedtuple("GraphScorePair", "graph head syntax_cost ontology_cost")


def get_semantic_trees(semantic_forest, head):
    assert isinstance(head, Type)
    head_key = head.id
    nodes = _get_nodes(semantic_forest, head_key)
    trees = [_node_to_tree(semantic_forest, node.children[0]) for node in nodes]
    tree_dict = {idx: tree for idx, tree in enumerate(trees)}
    return tree_dict


def _get_nodes(semantic_forest, head_key):
    head = semantic_forest.graph_nodes[head_key]
    if isinstance(head, GroundedToken) and isinstance(head.ground, Constant) or \
            isinstance(head, ImpliedInstance):
        node = Node(head_key, [], [])
        return [node]
    else:
        if isinstance(head, Type):
            nodes = []
            for u, v, edge_key in semantic_forest.forest_graph.edges(head_key, keys=True):
                children_nodes = _get_nodes(semantic_forest, v)
                for child_node in children_nodes:
                    new_node = Node(head_key, [child_node], [edge_key])
                    nodes.append(new_node)
            return nodes
        elif isinstance(head, GroundedToken) or isinstance(head, ImpliedSourceFunction):
            children_list = [[] for _ in range(head.ground.valence)]
            for u, v, edge_key, data in semantic_forest.forest_graph.edges(head_key, data=True, keys=True):
                arg_idx = data['arg_idx']
                new_nodes = _get_nodes(semantic_forest, v)
                new_pairs = [[new_node, edge_key] for new_node in new_nodes]
                children_list[arg_idx].extend(new_pairs)

            nodes = []
            for pairs in itertools.product(*children_list):
                arg_nodes, edge_keys = zip(*pairs)
                new_node = Node(head_key, arg_nodes, edge_keys)
                nodes.append(new_node)
            return nodes
        else:
            raise Exception()


def _node_to_tree(semantic_forest, node):
    graph = nx.DiGraph()
    _fill_graph(semantic_forest, graph, node, (0, ))
    formula = tree_graph_to_formula(semantic_forest, graph, node.head_key)
    tree = SemanticTree(semantic_forest, graph, formula)
    return tree

def _fill_graph(semantic_forest, graph, node, index):
    head = semantic_forest.graph_nodes[node.head_key]
    graph.add_node(index, label=head.label, key=node.head_key)
    for arg_idx, child in enumerate(node.children):
        new_index = index+(arg_idx,)
        _fill_graph(semantic_forest, graph, child, new_index)
        graph.add_edge(index, new_index, label="%d" % arg_idx, key=node.edge_keys[arg_idx])


class Node(object):
    def __init__(self, head_key, children, edge_keys):
        self.head_key = head_key
        self.children = children
        self.edge_keys = edge_keys
