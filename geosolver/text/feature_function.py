from geosolver.text.ontology import types
from geosolver.text.rule import UnaryRule, BinaryRule
import networkx as nx
import numpy as np
from geosolver.text.transitions import binary_rule_to_unary_rules

__author__ = 'minjoon'

def get_unary_feature_function(unary_rules, degree=1):
    """
    Change functions to add more dimensions

    :param unary_rules:
    :return:
    """
    functions = unary_generate(unary_rules)
    def out(unary_rule):
        return np.array([function(unary_rule) for function in functions])
    return out


def get_binary_feature_funtion(binary_rules, degree=1):
    functions = binary_generate(binary_rules)
    def out(binary_rule):
        return np.array([function(binary_rule) for function in functions])
    return out

def unary_generate(unary_rules):
    """
    Only add more functions here!

    :param unary_rules:
    :return:
    """
    functions = unary_generate_00(unary_rules) + unary_generate_01(unary_rules) + unary_generate_02(unary_rules)
    return functions


def binary_generate(binary_rules):
    """
    Don't change this!

    :param binary_rules:
    :return:
    """
    pairs = [binary_rule_to_unary_rules(binary_rule) for binary_rule in binary_rules]
    u1s, u2s, u3s = zip(*pairs)
    return unary_generate(u1s) + unary_generate(u2s) + unary_generate(u3s)

def unary_generate_00(unary_rules):
    """
    direct neighbors with edge label in syntax tree, both ways

    :param unary_rules:
    :return:
    """
    labels = set()
    for unary_rule in unary_rules:
        if unary_rule.parent_index in unary_rule.syntax_tree.undirected[unary_rule.child_index]:
            label = unary_rule.syntax_tree.undirected[unary_rule.parent_index][unary_rule.child_index]
            labels.add(label)

    functions = []
    for label in labels:
        def down(rule):
            if rule.child_index in rule.syntax_tree.directed[rule.parent_index] and \
                    rule.syntax_tree.directed[rule.parent_index][rule.child_index] == label:
                return 1
            else:
                return 0

        def up(rule):
            if rule.parent_index in rule.syntax_tree.directed[rule.child_index] and \
                            rule.syntax_tree.directed[rule.child_index][rule.parent_index] == label:
                return 1
            else:
                return 0
        functions.append(down)
        functions.append(up)
    return functions


def unary_generate_01(unary_rules):
    """
    return type of parent signature and child signature

    :param unary_rules:
    :return:
    """
    functions = []
    for type_ in types:
        def parent(rule):
            if rule.parent_signature.return_type == type_:
                return 1
            else:
                return 0

        def child(rule):
            if rule.child_signature.return_type == type_:
                return 1
            else:
                return 0
        functions.append(parent)
        functions.append(child)
    return functions


def unary_generate_02(unary_rules):
    distances = set()
    for unary_rule in unary_rules:
        if unary_rule.parent_index is not None and unary_rule.child_index is not None:
            distance = nx.shortest_path_length(unary_rule.syntax_tree.undirected, unary_rule.parent_index, unary_rule.child_index)
            distances.add(distance)

    functions = []
    for distance in distances:
        def function(rule):
            if rule.parent_index is not None and rule.child_index is not None:
                curr_distance = nx.shortest_path_length(rule.syntax_tree.undirected, rule.parent_index, rule.child_index)
                if curr_distance == distance:
                    return 1
            return 0
        functions.append(function)
    return functions




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
            d0 = len(unary_rule.words)
            d1 = d0

        i0 = int(unary_rule.child_signature.is_leaf())
        i1 = int(unary_rule.parent_index is None)
        out = np.array([d0, d1, i0, i1])
        assert len(out) == UFF1.dim
        return out


class UFF2(FeatureFunction):
    dim = 9
    @staticmethod
    def evaluate(unary_rule):
        assert isinstance(unary_rule, UnaryRule)
        if unary_rule.parent_index is not None and unary_rule.child_index is not None:
            d0 = abs(unary_rule.parent_index - unary_rule.child_index)
            t0 = nx.shortest_path_length(unary_rule.syntax_tree.undirected, unary_rule.parent_index, unary_rule.child_index)
        else:
            d0 = len(unary_rule.words)
            t0 = d0

        d1 = int(d0 == 1)
        d2 = int(d0 == 2)
        d3 = int(d0 >= 3)
        t1 = int(t0 == 1)
        t2 = int(t0 == 2)
        t3 = int(t0 >= 3)

        f1 = int(unary_rule.words.values()[-1] == ".")
        f2 = int(unary_rule.words.values()[-1] == "?")
        f3 = int(unary_rule.words.values()[-1] in ".?")
        out = np.array([d1,d2,d3,t1,t2,t3,f1,f2,f3])
        assert len(out) == UFF2.dim
        return out


class BFF1(FeatureFunction):
    dim = UFF2.dim*2 + 6
    @staticmethod
    def evaluate(binary_rule):
        assert isinstance(binary_rule, BinaryRule)
        unary_rule_a = UnaryRule(binary_rule.words, binary_rule.syntax_tree, binary_rule.tags, binary_rule.parent_index,
                             binary_rule.parent_signature, binary_rule.a_index, binary_rule.a_signature)
        unary_rule_b = UnaryRule(binary_rule.words, binary_rule.syntax_tree, binary_rule.tags, binary_rule.parent_index,
                             binary_rule.parent_signature, binary_rule.b_index, binary_rule.b_signature)
        a = UFF2.evaluate(unary_rule_a)
        b = UFF2.evaluate(unary_rule_b)


        if binary_rule.a_index is not None and binary_rule.b_index is not None:
            d0 = abs(binary_rule.a_index - binary_rule.b_index)
            t0 = nx.shortest_path_length(binary_rule.syntax_tree.undirected, binary_rule.a_index, binary_rule.b_index)
        else:
            d0 = len(binary_rule.words)
            t0 = d0

        d1 = int(d0 == 1)
        d2 = int(d0 == 2)
        d3 = int(d0 >= 3)
        t1 = int(t0 == 1)
        t2 = int(t0 == 2)
        t3 = int(t0 >= 3)
        my = np.array([d1,d2,d3,t1,t2,t3])

        out = np.concatenate([a, b, my])
        assert len(out) == BFF1.dim
        return out

