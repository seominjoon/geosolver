import itertools
from geosolver.text.ontology import types
from geosolver.text.rule import UnaryRule, BinaryRule
import networkx as nx
import numpy as np
from geosolver.text.transitions import binary_rule_to_unary_rules

__author__ = 'minjoon'


class FeatureFunction(object):
    def __init__(self, functions):
        self.dim = len(functions)
        self.functions = functions

    def evaluate(self, rule):
        return np.array([function(rule) for function in self.functions])


def unary_generator_00(unary_rules):
    """
    direct neighbors with edge label in syntax tree, both ways

    :param unary_rules:
    :return:
    """
    labels = set()
    for unary_rule in unary_rules:
        if unary_rule.parent_index is None or unary_rule.child_index is None:
            continue
        if unary_rule.parent_index in unary_rule.syntax_tree.undirected[unary_rule.child_index]:
            label = unary_rule.syntax_tree.undirected[unary_rule.parent_index][unary_rule.child_index]['label']
            labels.add(label)

    print "labels:", labels

    functions = []
    for label in labels:
        functions.append(_get_down(label))
        functions.append(_get_up(label))
    return functions

def _get_down(label):
    def down(rule):
        if rule.child_index is None or rule.parent_index is None:
            return 0
        if rule.child_index in rule.syntax_tree.directed[rule.parent_index] and \
                        rule.syntax_tree.directed[rule.parent_index][rule.child_index]['label'] == label:
            return 1
        else:
            return 0
    return down

def _get_up(label):
    def up(rule):
        if rule.child_index is None or rule.parent_index is None:
            return 0
        if rule.parent_index in rule.syntax_tree.directed[rule.child_index] and \
                        rule.syntax_tree.directed[rule.child_index][rule.parent_index]['label'] == label:
            return 1
        else:
            return 0
    return up

def unary_generator_01(unary_rules):
    """
    return type of parent content and child content

    :param unary_rules:
    :return:
    """
    functions = []
    for type_ in types:
        functions.append(_get_parent(type_))
        functions.append(_get_child(type_))
    return functions


def _get_parent(type_):
    def parent(rule):
        if rule.parent_signature.return_type == type_:
            return 1
        else:
            return 0
    return parent


def _get_child(type_):
    def child(rule):
        if rule.child_signature.return_type == type_:
            return 1
        else:
            return 0
    return child


def unary_generator_02(unary_rules):
    distances = set()
    for unary_rule in unary_rules:
        if unary_rule.parent_index is not None and unary_rule.child_index is not None:
            distance = nx.shortest_path_length(unary_rule.syntax_tree.undirected, unary_rule.parent_index, unary_rule.child_index)
            distances.add(distance)

    print "distances:", distances

    functions = []
    for distance in distances:
        functions.append(_get_df(distance))
    return functions

def _get_df(distance):
    def df(rule):
        if rule.parent_index is not None and rule.child_index is not None:
            curr_distance = nx.shortest_path_length(rule.syntax_tree.undirected, rule.parent_index, rule.child_index)
            if curr_distance == distance:
                return 1
        return 0
    return df

unary_generators = [unary_generator_00, unary_generator_01, unary_generator_02]

def generate_unary_feature_function(rules):
    functions = list(itertools.chain(*[generator(rules) for generator in unary_generators]))
    print "functions:", functions
    feature_function = FeatureFunction(functions)
    return feature_function


def generate_binary_feature_function(rules):
    a_rules, b_rules, c_rules = zip(*(rule.unary_rules for rule in rules))
    a_functions = list(itertools.chain(*[unary_generator(a_rules) for unary_generator in unary_generators]))
    b_functions = list(itertools.chain(*[unary_generator(b_rules) for unary_generator in unary_generators]))
    c_functions = list(itertools.chain(*[unary_generator(c_rules) for unary_generator in unary_generators]))
    binary_a_functions = [lambda binary_rule: a_function(binary_rule.a_rule) for a_function in a_functions]
    binary_b_functions = [lambda binary_rule: b_function(binary_rule.b_rule) for b_function in b_functions]
    binary_c_functions = [lambda binary_rule: c_function(binary_rule.c_rule) for c_function in c_functions]
    functions = binary_a_functions + binary_b_functions + binary_c_functions
    feature_function = FeatureFunction(functions)
    return feature_function
