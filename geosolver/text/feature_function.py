from geosolver.text.rule import UnaryRule, BinaryRule
import networkx as nx
import numpy as np
from geosolver.utils import display_graph

__author__ = 'minjoon'


class FeatureFunction(object):
    dim = 0
    def __init__(self):
        pass

    @staticmethod
    def evaluate(rule):
        pass

class UFF1(FeatureFunction):
    dim = 4
    @staticmethod
    def evaluate(unary_rule):
        # For now, just distance between them in dependency tree and sentence and their product
        assert isinstance(unary_rule, UnaryRule)
        if unary_rule.parent_index is not None and unary_rule.child_index is not None:
            d0 = abs(unary_rule.parent_index - unary_rule.child_index)
            d1 = nx.shortest_path_length(unary_rule.syntax_tree.undirected, unary_rule.parent_index, unary_rule.child_index)
        else:
            d0 = len(unary_rule.words)/2.0
            d1 = d0

        i0 = int(unary_rule.child_signature.is_leaf())
        i1 = int(unary_rule.parent_index is None)
        out = np.array([d0, d1, i0, i1])
        assert len(out) == UFF1.dim
        return out


class BFF1(FeatureFunction):
    dim = UFF1.dim*2 + 2
    @staticmethod
    def evaluate(binary_rule):
        assert isinstance(binary_rule, BinaryRule)
        unary_rule_a = UnaryRule(binary_rule.words, binary_rule.syntax_tree, binary_rule.tags, binary_rule.parent_index,
                             binary_rule.parent_signature, binary_rule.a_index, binary_rule.a_signature)
        unary_rule_b = UnaryRule(binary_rule.words, binary_rule.syntax_tree, binary_rule.tags, binary_rule.parent_index,
                             binary_rule.parent_signature, binary_rule.b_index, binary_rule.b_signature)
        a = UFF1.evaluate(unary_rule_a)
        b = UFF1.evaluate(unary_rule_b)


        if binary_rule.a_index is not None and binary_rule.b_index is not None:
            d0 = abs(binary_rule.a_index - binary_rule.b_index)
            d1 = nx.shortest_path_length(binary_rule.syntax_tree.undirected, binary_rule.a_index, binary_rule.b_index)
        else:
            d0 = len(binary_rule.words)/2.0
            d1 = d0
        my = np.array([d0, d1])

        out = np.concatenate([a, b, my])
        assert len(out) == BFF1.dim
        return out

