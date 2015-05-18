from geosolver.text2.get_annotation_tree import AnnotationNode

__author__ = 'minjoon'

def annotation_tree_to_tag_rules(syntax_parse, annotation_tree):
    pass


def annotation_tree_to_semantic_rules(syntax_parse, annotation_tree):
    conj_rules = []
    is_rules = []
    unary_rules = []
    binary_rules = []
    for annotation_node in annotation_tree:
        assert isinstance(annotation_node, AnnotationNode)


