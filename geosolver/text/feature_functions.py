import itertools
from geosolver.text.rule import UnaryRule, BinaryRule
import numpy as np

__author__ = 'minjoon'

UNARY_FEATURE_DIMENSION = 5
BINARY_FEATURE_DIMENSION = 2*UNARY_FEATURE_DIMENSION + 3

def uff1(unary_rule):
    # For now, just distance between them in dependency tree and sentence and their product
    assert isinstance(unary_rule, UnaryRule)
    if unary_rule.parent_index is not None and unary_rule.child_index is not None:
        f2 = abs(unary_rule.parent_index - unary_rule.child_index)
        # f1 = nx.shortest_path_length(unary_rule.syntax_tree, unary_rule.parent_index, unary_rule.child_index)
        f1 = f2
    else:
        f1 = len(unary_rule.words)/2.0
        f2 = f1
    f3 = np.sqrt(f1*f2)
    f4 = int(unary_rule.child_signature.is_leaf())
    f5 = int(unary_rule.parent_index is None)
    out = np.array([f1, f2, f3, f4, f5])
    assert len(out) == UNARY_FEATURE_DIMENSION
    return out


def bff1(binary_rule):
    """
    binary feature function version 1
    Usually, this will depend on unary feature function.

    :param binary_rule:
    :return:
    """
    assert isinstance(binary_rule, BinaryRule)
    unary_rule_a = UnaryRule(binary_rule.words, binary_rule.syntax_tree, binary_rule.tags, binary_rule.parent_index,
                             binary_rule.parent_signature, binary_rule.a_index, binary_rule.a_signature)
    unary_rule_b = UnaryRule(binary_rule.words, binary_rule.syntax_tree, binary_rule.tags, binary_rule.parent_index,
                             binary_rule.parent_signature, binary_rule.b_index, binary_rule.b_signature)
    if binary_rule.a_index is not None and binary_rule.b_index is not None:
        f2 = abs(binary_rule.a_index - binary_rule.b_index)
        # f1 = nx.shortest_path_length(binary_rule.syntax_tree, binary_rule.a_index, binary_rule.b_index)
        f1 = f2**2
    else:
        f1 = len(binary_rule.words)/2.0
        f2 = f1**2
    f3 = np.sqrt(f1*f2)

    a1 = uff1(unary_rule_a)
    a2 = uff1(unary_rule_b)
    a3 = [f1, f2, f3]

    out = np.array(list(itertools.chain(a1, a2, a3)))
    assert len(out) == BINARY_FEATURE_DIMENSION
    return out
