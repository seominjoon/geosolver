from collections import deque
import itertools
from geosolver.text.node import Node
from geosolver.text.ontology import function_signatures, issubtype
from geosolver.text.ontology_states import FunctionSignature
from geosolver.text.rule import TagRule, UnaryRule, BinaryRule

__author__ = 'minjoon'

def tuple_to_tag_rules(words, syntax_tree, tuple_):
    splitter = '@'
    implication = 'i'
    tag_rules = []
    for string in tuple_:
        function_name, index = string.split(splitter)
        if function_name in function_signatures:
            function_signature = function_signatures[function_name]
        elif (function_name[0], function_name[-1]) == tuple("''"):
            function_signature = FunctionSignature(function_name[1:-1], 'modifier', [])
        elif (function_name[0], function_name[-1]) == tuple("[]"):
            function_signature = FunctionSignature(function_name[1:-1], 'number', [])
        elif (function_name[0], function_name[-1]) == tuple("<>"):
            function_signature = FunctionSignature(function_name[1:-1], 'variable', [])
        else:
            raise Exception()

        if index == implication:
            index = None
        else:
            index = int(index)
        tag_rule = TagRule(words, syntax_tree, index, function_signature)
        tag_rules.append(tag_rule)
    return tag_rules


def tuples_to_semantic_rules(words, syntax_tree, tuples):
    # TODO : index inheritance
    tag_rules_list = [tuple_to_tag_rules(words, syntax_tree, tuple_) for tuple_ in tuples]
    tags = {tag_rule.index: tag_rule.signature for tag_rule in itertools.chain(*tag_rules_list)}
    for index in words:
        if index not in tags:
            tags[index] = None

    unary_rules = []
    binary_rules = []
    for tag_rules in tag_rules_list:
        if len(tag_rules) == 2:
            unary_rule = UnaryRule(words, syntax_tree, tags, tag_rules[0].index, tag_rules[0].signature,
                                   tag_rules[1].index, tag_rules[1].signature)
            unary_rules.append(unary_rule)
        elif len(tag_rules) == 3:
            binary_rule = BinaryRule(words, syntax_tree, tags, tag_rules[0].index, tag_rules[0].signature,
                                     tag_rules[1].index, tag_rules[1].signature,
                                     tag_rules[2].index, tag_rules[2].signature)
            binary_rules.append(binary_rule)
    return unary_rules, binary_rules


def node_to_semantic_rules(words, syntax_tree, tags, node, lift_index=False):
    assert isinstance(node, Node)
    unary_rules = []
    binary_rules = []
    """
    if issubtype(node.function_signature.return_type, 'truth'):
        start_rule = UnaryRule(words, syntax_tree, tags, None, function_signatures['StartTruth'], node.index, node.function_signature)
    else:
        print node.function_signature
        start_rule = None
        raise Exception()
    unary_rules.append(start_rule)
    """


    stack = deque()
    stack.appendleft(node)
    while len(stack) > 0:
        curr_node = stack.pop()
        assert isinstance(curr_node, Node)
        if curr_node.function_signature.is_leaf():
            continue
        elif curr_node.function_signature.is_unary():
            child_node = curr_node.children[0]
            unary_rule = UnaryRule(words, syntax_tree, tags, curr_node.index, curr_node.function_signature,
                                   child_node.get_index(lift_index), child_node.function_signature)
            unary_rules.append(unary_rule)
            stack.appendleft(child_node)
        elif curr_node.function_signature.is_binary():
            a_node, b_node = curr_node.children
            binary_rule = BinaryRule(words, syntax_tree, tags, curr_node.index, curr_node.function_signature,
                                     a_node.get_index(lift_index), a_node.function_signature,
                                     b_node.get_index(lift_index), b_node.function_signature)
            binary_rules.append(binary_rule)
            stack.appendleft(a_node)
            stack.appendleft(b_node)
    return unary_rules, binary_rules


def node_to_tag_rules(words, syntax_tree, node):
    assert isinstance(node, Node)
    tag_rules = []
    for index, sig in node.iterate():
        if index is not None:
            tag_rule = TagRule(words, syntax_tree, index, sig)
            tag_rules.append(tag_rule)
    return tag_rules


def tag_rules_to_tags(words, tag_rules):
    """
    a list of tag rules --> tags for single sentence
    :param tag_rules:
    :return:
    """
    tags = {index: None for index in words}
    if len(tag_rules) == 0:
        return tags
    for tag_rule in tag_rules:
        assert isinstance(tag_rule, TagRule)
        tags[tag_rule.index] = tag_rule.signature
    return tags


def string_to_words(string):
    word_list = string.split(' ')
    words = {index: word_list[index] for index in range(len(word_list))}
    return words


def binary_rule_to_unary_rules(rule):
    """
    transform a binary rule to three unary rules, namely
    parent-left, parent-right, left-right

    :param binary_rule:
    :return:
    """
    parent_left = UnaryRule(rule.words, rule.syntax_tree, rule.tags, rule.parent_index, rule.parent_signature, rule.a_index, rule.b_signature)
    parent_right = UnaryRule(rule.words, rule.syntax_tree, rule.tags, rule.parent_index, rule.parent_signature, rule.b_index, rule.b_signature)
    left_right = UnaryRule(rule.words, rule.syntax_tree, rule.tags, rule.a_index, rule.a_signature, rule.b_index, rule.b_signature)
    return parent_left, parent_right, left_right


def semantic_rule_to_tag_rules(semantic_rule):
    tag_rules = []
    tag_rules.append(TagRule(semantic_rule.words, semantic_rule.syntax_tree, semantic_rule.parent_index, semantic_rule.parent_signature))

    if isinstance(semantic_rule, UnaryRule):
        tag_rules.append(TagRule(semantic_rule.words, semantic_rule.syntax_tree, semantic_rule.child_index, semantic_rule.child_signature))
    if isinstance(semantic_rule, BinaryRule):
        tag_rules.append(TagRule(semantic_rule.words, semantic_rule.syntax_tree, semantic_rule.a_index, semantic_rule.a_signature))
        tag_rules.append(TagRule(semantic_rule.words, semantic_rule.syntax_tree, semantic_rule.b_index, semantic_rule.b_signature))
    return tag_rules


def rules_to_impliable_signatures(rules):
    impliable_signatures = set()
    for rule in rules:
        if isinstance(rule, UnaryRule):
            if rule.parent_index is None:
                impliable_signatures.add(rule.parent_signature)
            if rule.child_index is None:
                impliable_signatures.add(rule.child_signature)
        elif isinstance(rule, BinaryRule):
            if rule.parent_index is None:
                impliable_signatures.add(rule.parent_signature)
            if rule.a_index is None:
                impliable_signatures.add(rule.a_signature)
            if rule.b_index is None:
                impliable_signatures.add(rule.b_signature)
    return impliable_signatures
