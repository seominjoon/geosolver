from geosolver.text2.get_annotation_tree import AnnotationNode
from geosolver.text2.rule import UnaryRule

__author__ = 'minjoon'

def annotation_tree_to_tag_rules(syntax_parse, annotation_tree):
    return [annotation_node.content for annotation_node in annotation_tree
            if annotation_node.content.span != "i"]


def annotation_tree_to_semantic_rules(syntax_parse, annotation_tree):
    conj_rules = []
    is_rules = []
    unary_rules = []
    binary_rules = []
    implication_rules = []
    for annotation_node in annotation_tree:
        a_tag_rule = annotation_node.content
        assert isinstance(annotation_node, AnnotationNode)
        if annotation_node.valence == 1:
            child_node = annotation_node.children[0]
            b_tag_rule = _get_first_explicit_descendant(child_node)
            unary_rule = UnaryRule(syntax_parse, a_tag_rule, b_tag_rule)
            unary_rules.append(unary_rule)
    return unary_rules


def _get_first_explicit_descendant(annotation_node):
    while annotation_node.content.is_implicit:
        annotation_node = annotation_node.children[0]
    return annotation_node