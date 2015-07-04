from geosolver import geoserver_interface
from geosolver.diagram.shortcuts import diagram_to_graph_parse
from geosolver.grounding.ground_formula_nodes import ground_formula_nodes
from geosolver.grounding.parse_match_from_known_labels import parse_match_from_known_labels
from geosolver.text2.annotation_node_to_rules import annotation_node_to_tag_rules, annotation_node_to_semantic_rules
from geosolver.text2.get_annotation_node import get_annotation_node, is_valid_annotation
from geosolver.text2.post_processing import apply_trans, filter_dummies, apply_cc, apply_distribution
from geosolver.text2.syntax_parser import SyntaxParse
from geosolver.utils.prep import open_image

__author__ = 'minjoon'

def test_validity():
    questions = geoserver_interface.download_questions(1014)
    annotations = geoserver_interface.download_semantics(1014)
    all_tag_rules = []
    all_unary_rules = []
    all_binary_rules = []
    for pk, question in questions.iteritems():
        for number, words in question.words.iteritems():
            syntax_parse = SyntaxParse(words, None)
            local_annotations = annotations[pk][number]
            for _, annotation in local_annotations.iteritems():
                if is_valid_annotation(syntax_parse, annotation):

                    node = get_annotation_node(syntax_parse, annotation)
                    formula = node.to_formula()
                    print "formula:", formula
                    tag_rules = annotation_node_to_tag_rules(node)
                    unary_rules, binary_rules = annotation_node_to_semantic_rules(node)
                    all_tag_rules.extend(tag_rules)
                    all_unary_rules.extend(unary_rules)
                    all_binary_rules.extend(binary_rules)
                else:
                    print annotation

def test_trans():
    query = 995
    questions = geoserver_interface.download_questions(query)
    annotations = geoserver_interface.download_semantics(query)
    for pk, question in questions.iteritems():
        label_data = geoserver_interface.download_labels(pk)[pk]
        diagram = open_image(question.diagram_path)
        graph_parse = diagram_to_graph_parse(diagram)
        match_parse = parse_match_from_known_labels(graph_parse, label_data)
        for number, words in question.words.iteritems():
            syntax_parse = SyntaxParse(words, None)
            nodes = [get_annotation_node(syntax_parse, annotation) for annotation in annotations[pk][number].values()]
            formulas = [node.to_formula() for node in nodes]
            new_formulas = apply_trans(None, formulas)
            new_formulas = filter_dummies(new_formulas)
            new_formulas = apply_cc(new_formulas)
            new_formulas = ground_formula_nodes(match_parse, new_formulas)
            new_formulas = apply_distribution(new_formulas)
            for new_formula in new_formulas:
                print new_formula
        graph_parse.core_parse.display_points()



if __name__ == "__main__":
    test_trans()
    # test_validity()
