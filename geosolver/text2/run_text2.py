from geosolver import geoserver_interface
from geosolver.text2.annotation_node_to_rules import annotation_node_to_tag_rules, annotation_node_to_semantic_rules
from geosolver.text2.get_annotation_node import get_annotation_node, is_valid_annotation
from geosolver.text2.syntax_parser import SyntaxParse

__author__ = 'minjoon'

def test_validity():
    questions = geoserver_interface.download_questions('test')
    annotations = geoserver_interface.download_semantics('test')
    all_tag_rules = []
    all_unary_rules = []
    all_binary_rules = []
    for pk, question in questions.iteritems():
        for number, words in question.words.iteritems():
            local_annotations = annotations[pk][number]
            for _, annotation in local_annotations.iteritems():
                syntax_parse = SyntaxParse(words, None)
                if is_valid_annotation(syntax_parse, annotation):

                    node = get_annotation_node(syntax_parse, annotation)
                    tag_rules = annotation_node_to_tag_rules(node)
                    unary_rules, binary_rules = annotation_node_to_semantic_rules(node)
                    all_tag_rules.extend(tag_rules)
                    all_unary_rules.extend(unary_rules)
                    all_binary_rules.extend(binary_rules)
                else:
                    print annotation


if __name__ == "__main__":
    test_validity()
