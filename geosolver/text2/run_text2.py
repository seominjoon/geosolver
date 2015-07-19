from geosolver import geoserver_interface
from geosolver.diagram.parse_confident_atoms import parse_confident_atoms
from geosolver.diagram.shortcuts import diagram_to_graph_parse
from geosolver.expression.expression_parser import expression_parser
from geosolver.expression.prefix_to_formula import prefix_to_formula
from geosolver.grounding.ground_formula_nodes import ground_formula_node
from geosolver.grounding.parse_match_atoms import parse_match_atoms
from geosolver.grounding.parse_match_from_known_labels import parse_match_from_known_labels
from geosolver.ontology.ontology_semantics import evaluate
from geosolver.solver.solve import solve
from geosolver.text2.annotation_node_to_rules import annotation_node_to_tag_rules, annotation_node_to_semantic_rules
from geosolver.text2.annotation_nodes_to_text_formula_parse import annotation_nodes_to_text_formula_parse
from geosolver.text2.get_annotation_node import get_annotation_node, is_valid_annotation
from geosolver.text2.complete_text_formula_parse import complete_text_formula_parse
from geosolver.text2.syntax_parser import SyntaxParse
from geosolver.ontology.utils import filter_formulas, reduce_formulas
from geosolver.ontology.utils import flatten_formulas
from geosolver.utils.prep import open_image
import pyipopt


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
    query = 1043
    questions = geoserver_interface.download_questions(query)
    all_annotations = geoserver_interface.download_semantics(query)
    for pk, question in questions.iteritems():
        choice_formulas = get_choice_formulas(question)
        label_data = geoserver_interface.download_labels(pk)[pk]
        diagram = open_image(question.diagram_path)
        graph_parse = diagram_to_graph_parse(diagram)
        core_parse = graph_parse.core_parse
        match_parse = parse_match_from_known_labels(graph_parse, label_data)
        match_formulas = parse_match_atoms(match_parse)
        diagram_formulas = parse_confident_atoms(graph_parse)
        all_formulas = match_formulas + diagram_formulas
        for number, sentence_words in question.sentence_words.iteritems():
            syntax_parse = SyntaxParse(sentence_words, None)
            annotation_nodes = [get_annotation_node(syntax_parse, annotation)
                                for annotation in all_annotations[pk][number].values()]
            expr_formulas = [prefix_to_formula(expression_parser.parse_prefix(expression))
                             for expression in question.sentence_expressions[number].values()]
            text_formula_parse = annotation_nodes_to_text_formula_parse(annotation_nodes)
            completed_formulas = complete_text_formula_parse(text_formula_parse)
            grounded_formulas = [ground_formula_node(match_parse, formula) for formula in completed_formulas+expr_formulas]
            text_formulas = filter_formulas(flatten_formulas(grounded_formulas))
            all_formulas.extend(text_formulas)

        reduced_formulas = reduce_formulas(all_formulas)
        for reduced_formula in reduced_formulas:
            if reduced_formula.is_grounded(core_parse.variable_assignment.keys()):
                score = evaluate(reduced_formula, core_parse.variable_assignment)
                scores = [evaluate(child, core_parse.variable_assignment) for child in reduced_formula.children]
            else:
                score = None
                scores = None
            print reduced_formula, score, scores
        result = solve(reduced_formulas, choice_formulas, assignment=core_parse.variable_assignment)
        print result

        graph_parse.core_parse.display_points()


def get_choice_formulas(question):
    """
    Temporary; will be replaced by text parser
    :param question:
    :return:
    """
    choice_formulas = {}
    for number, choice_expressions in question.choice_expressions.iteritems():
        choice_words = question.choice_words[number]
        if len(choice_expressions) == 1:
            string = choice_expressions.values()[0]
        elif len(choice_expressions) == 0:
            string = choice_words.values()[0]
        else:
            return None
        expr_formula = prefix_to_formula(expression_parser.parse_prefix(string))
        choice_formulas[number] = expr_formula
    if len(choice_formulas) == 0:
        return None
    return choice_formulas


if __name__ == "__main__":
    test_trans()
    # test_validity()
