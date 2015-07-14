from geosolver import geoserver_interface
from geosolver.diagram.shortcuts import diagram_to_graph_parse
from geosolver.grounding.ground_formula_nodes import ground_formula_node
from geosolver.grounding.parse_match_from_known_labels import parse_match_from_known_labels
from geosolver.ontology.ontology_semantics import evaluate
from geosolver.text2.annotation_node_to_rules import annotation_node_to_tag_rules, annotation_node_to_semantic_rules
from geosolver.text2.annotation_nodes_to_text_formula_parse import annotation_nodes_to_text_formula_parse
from geosolver.text2.get_annotation_node import get_annotation_node, is_valid_annotation
from geosolver.text2.complete_text_formula_parse import complete_text_formula_parse
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
    query = 1058
    questions = geoserver_interface.download_questions(query)
    all_annotations = geoserver_interface.download_semantics(query)
    for pk, question in questions.iteritems():
        label_data = geoserver_interface.download_labels(pk)[pk]
        diagram = open_image(question.diagram_path)
        graph_parse = diagram_to_graph_parse(diagram)
        match_parse = parse_match_from_known_labels(graph_parse, label_data)
        for number, sentence_words in question.sentence_words.iteritems():
            syntax_parse = SyntaxParse(sentence_words, None)
            annotation_nodes = [get_annotation_node(syntax_parse, annotation)
                                for annotation in all_annotations[pk][number].values()]
            text_formula_parse = annotation_nodes_to_text_formula_parse(annotation_nodes)
            completed_formulas = complete_text_formula_parse(text_formula_parse)
            for formula in completed_formulas:
                grounded_formula = ground_formula_node(match_parse, formula)
                if grounded_formula.is_grounded(graph_parse.core_parse.variable_assignment.keys()):
                    score = evaluate(grounded_formula, graph_parse.core_parse.variable_assignment)
                else:
                    score = None
                print grounded_formula, score

        graph_parse.core_parse.display_points()



if __name__ == "__main__":
    test_trans()
    # test_validity()
