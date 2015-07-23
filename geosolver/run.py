from cStringIO import StringIO
import logging
import numbers
import sys
import time
from geosolver import geoserver_interface
from geosolver.diagram.parse_confident_formulas import parse_confident_formulas
from geosolver.diagram.shortcuts import diagram_to_graph_parse
from geosolver.expression.expression_parser import expression_parser
from geosolver.expression.prefix_to_formula import prefix_to_formula
from geosolver.grounding.ground_formula_nodes import ground_formula_node
from geosolver.grounding.parse_match_atoms import parse_match_atoms
from geosolver.grounding.parse_match_from_known_labels import parse_match_from_known_labels
from geosolver.ontology.ontology_definitions import FormulaNode
from geosolver.ontology.ontology_definitions import signatures
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

__author__ = 'minjoon'


class SimpleResult(object):
    def __init__(self, id_, error, attempted, correct, duration=-1, message=""):
        assert isinstance(attempted, bool)
        assert isinstance(correct, bool)
        assert isinstance(error, bool)
        assert isinstance(duration, numbers.Real)
        assert isinstance(message, str)
        assert attempted or not correct
        self.id = id_
        self.attempted = attempted
        self.correct = correct
        self.duration = duration
        self.message = message
        self.error = error

    def __repr__(self):
        return "(e,a,c) = %s, %s, %s" % (self.error, self.attempted, self.correct)

def annotated_unit_test(query):
    """
    Attempts to solve the question with id=id_.
    If the answer is correct, return 'c'
    If the answer is wrong, return 'i'
    If an error occurred, return 'e'

    :param id_:
    :return SimpleResult:
    """
    #myout = StringIO()
    #oldstdout = sys.stdout
    #sys.stdout = myout
    try:
        result = _annotated_unit_test(query)
    except Exception, e:
        logging.exception(e)
        result = SimpleResult(query, True, False, False)
    #sys.stdout = oldstdout
    #message = myout.getvalue()
    #result.message = message
    return result

def _annotated_unit_test(query):
    questions = geoserver_interface.download_questions(query)
    all_annotations = geoserver_interface.download_semantics(query)
    pk, question = questions.items()[0]

    choice_formulas = get_choice_formulas(question)
    label_data = geoserver_interface.download_labels(pk)[pk]
    diagram = open_image(question.diagram_path)
    graph_parse = diagram_to_graph_parse(diagram)
    core_parse = graph_parse.core_parse
    match_parse = parse_match_from_known_labels(graph_parse, label_data)
    match_formulas = parse_match_atoms(match_parse)
    diagram_formulas = parse_confident_formulas(graph_parse)
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
    ans = solve(reduced_formulas, choice_formulas, assignment=core_parse.variable_assignment)
    print "ans: %s" % ans

    if choice_formulas is None:
        attempted = True
        if abs(ans - float(question.answer)) < 0.01:
            correct = True
        else:
            correct = False
    else:
        attempted = True
        c = max(ans.iteritems(), key=lambda pair: pair[1].conf)[0]
        if c == int(question.answer):
            correct = True
        else:
            correct = False

    result = SimpleResult(query, False, attempted, correct)
    return result

    # graph_parse.core_parse.display_points()

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
            if len(choice_words) == 1:
                string = choice_words.values()[0]
            else:
                continue
                # string = r"\none"
        else:
            return None
        expr_formula = prefix_to_formula(expression_parser.parse_prefix(string))
        choice_formulas[number] = expr_formula
    if len(choice_formulas) == 0:
        return None
    return choice_formulas


def annotated_test():
    ids = [963, 968, 969, 971, 973, 974, 977, 985, 990, 993, 995, 1000, 1003, 1004, 1006, 1011, 1014, 1017, 1018, 1020,]
    # ids = [1017]
    correct = 0
    attempted = 0
    total = len(ids)
    error = 0
    start = time.time()
    for id_ in ids:
        id_ = str(id_)
        print "-"*80
        print "id: %s" % id_
        result = annotated_unit_test(id_)
        print result.message
        print result
        if result.error:
            error += 1
        if result.attempted:
            attempted += 1
        if result.correct:
            correct += 1
    end = time.time()
    print "-"*80
    print "duration:\t%.1f" % (end - start)

    out = "total:\t\t%d\nattempted:\t%d\ncorrect:\t%d\nerror:\t\t%d" % (total, attempted, correct, error)
    print out


if __name__ == "__main__":
    annotated_test()
