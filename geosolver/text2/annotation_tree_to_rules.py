from geosolver.text2.get_annotation_tree import AnnotationNode
from geosolver.text2.ontology import function_signatures
from geosolver.text2.rule import UnaryRule, ImplicationRule, IsRule, ConjRule, BinaryRule

__author__ = 'minjoon'

def annotation_tree_to_tag_rules(syntax_parse, annotation_tree):
    return [annotation_node.content for annotation_node in annotation_tree
            if annotation_node.content.span != "i"]


def annotation_tree_to_semantic_rules(syntax_parse, annotation_tree):
    unary_rules = []
    binary_rules = []
    conj_rules = []
    is_rules = []
    implication_rules = []
    for annotation_node in annotation_tree:
        a_tag_rule = annotation_node.content
        assert isinstance(annotation_node, AnnotationNode)
        if annotation_node.valence == 1:
            child_node = annotation_node.children[0]
            # unary rule
            b_tag_rule = _get_first_explicit_descendant(child_node).content
            unary_rule = UnaryRule(syntax_parse, a_tag_rule, b_tag_rule)
            unary_rules.append(unary_rule)

        elif annotation_node.valence == 2:
            b_node, c_node = annotation_node.children
            b_tag_rule = b_node.content
            c_tag_rule = c_node.content
            if a_tag_rule.signature == function_signatures['Is']:
                is_rule = IsRule(syntax_parse, b_tag_rule, c_tag_rule)
                is_rules.append(is_rule)
            elif a_tag_rule.signature == function_signatures['Conj']:
                conj_rule = ConjRule(syntax_parse, b_tag_rule, c_tag_rule)
                conj_rules.append(conj_rule)
            else:
                assert a_tag_rule.span != "i"
                binary_rule = BinaryRule(syntax_parse, a_tag_rule, b_tag_rule, c_tag_rule)
                binary_rules.append(binary_rule)

        # implication rule
        for arg_idx, child_node in enumerate(annotation_node.children):
            if child_node.content.is_implicit:
                b_tag_rule = _get_first_explicit_descendant(child_node)
                implied_tag_rules = _get_implied_tag_rules(child_node)
                implication_rule = ImplicationRule(syntax_parse, a_tag_rule, arg_idx, implied_tag_rules, b_tag_rule)
                implication_rules.append(implication_rule)

    return unary_rules, binary_rules, conj_rules, is_rules, implication_rules


def _get_first_explicit_descendant(annotation_node):
    while annotation_node.content.is_implicit:
        annotation_node = annotation_node.children[0]
    return annotation_node


def _get_implied_tag_rules(annotation_node):
    implied_tag_rules = []
    while annotation_node.content.is_implicit:
        implied_tag_rules.append(annotation_node.content)
        annotation_node = annotation_node.children[0]
    return implied_tag_rules
