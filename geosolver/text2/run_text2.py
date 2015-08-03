import itertools
import os
from pprint import pprint
import sys
from geosolver import geoserver_interface
from geosolver.text2.annotation_to_semantic_tree import annotation_to_semantic_tree, is_valid_annotation
from geosolver.text2.model import NaiveTagModel, UnaryModel, NaiveUnaryModel, NaiveBinaryModel
from geosolver.text2.semantic_forest import SemanticForest
from geosolver.text2.syntax_parser import SyntaxParse, stanford_parser
import numpy as np


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

                    node = annotation_to_semantic_tree(syntax_parse, annotation)
                    formula = node.to_formula()
                    print "formula:", formula
                    # tag_rules = annotation_node_to_tag_rules(node)
                    # unary_rules, binary_rules = annotation_node_to_semantic_rules(node)
                    # all_tag_rules.extend(tag_rules)
                    # all_unary_rules.extend(unary_rules)
                    # all_binary_rules.extend(binary_rules)
                else:
                    print annotation

def test_annotations_to_rules():
    questions = geoserver_interface.download_questions('test')
    all_annotations = geoserver_interface.download_semantics('test')
    print "parsing syntax..."
    syntax_parses = {pk: {number: stanford_parser.get_best_syntax_parse(words)
                          for number, words in question.sentence_words.iteritems()}
                     for pk, question in questions.iteritems()}

    all_tag_rules = []

    for pk, question in questions.iteritems():
        for number, sentence_words in question.sentence_words.iteritems():
            syntax_parse = syntax_parses[pk][number]
            semantic_trees = [annotation_to_semantic_tree(syntax_parse, annotation)
                              for annotation in all_annotations[pk][number].values()]
            tag_rules = itertools.chain(*[semantic_tree.get_tag_rules() for semantic_tree in semantic_trees])
            all_tag_rules.extend(tag_rules)
            # test = NaiveTagModel(all_tag_rules)
    tag_model = NaiveTagModel(all_tag_rules)

    # tag_model.print_lexicon()

    tree_nums = []
    for pk, question in questions.iteritems():
        print pk
        for number, sentence_words in question.sentence_words.iteritems():
            syntax_parse = syntax_parses[pk][number]
            semantic_trees = [annotation_to_semantic_tree(syntax_parse, annotation)
                              for annotation in all_annotations[pk][number].values()]
            true_unary_rules = set(itertools.chain(*[semantic_tree.get_unary_rules() for semantic_tree in semantic_trees]))
            true_binary_rules = set(itertools.chain(*[semantic_tree.get_binary_rules() for semantic_tree in semantic_trees]))
            tag_rules = tag_model.generate_tag_rules(syntax_parse)
            tag_rules = [x for x in tag_rules if x.signature.id not in ('Is', 'CC')]
            unary_model = NaiveUnaryModel(3)
            unary_rules = [ur for ur in unary_model.generate_unary_rules(tag_rules) if unary_model.get_score(ur) > 0]
            """
            for unary_rule in unary_rules:
                print unary_rule, unary_rule in true_unary_rules
            """

            binary_model = NaiveBinaryModel(3)
            binary_rules = [br for br in binary_model.generate_binary_rules(tag_rules) if binary_model.get_score(br) > 0]
            """
            for binary_rule in binary_rules:
                print binary_rule, binary_rule in true_binary_rules
            """
            semantic_forest = SemanticForest(tag_rules, unary_rules, binary_rules)
            semantic_trees = semantic_forest.get_semantic_trees_by_type("number")
            print ""

            for semantic_tree in semantic_trees:
                print semantic_tree

            tree_nums.append(len(semantic_trees))


            """
            for tag_rule in tag_rules:
                print tag_rule
            """
        print "\n\n"

    print min(tree_nums), np.mean(tree_nums), max(tree_nums)




if __name__ == "__main__":
    # test_validity()
    test_annotations_to_rules()
