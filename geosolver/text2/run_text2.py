import itertools
import os
from pprint import pprint
import sys
from geosolver import geoserver_interface
from geosolver.text2.annotation_to_semantic_tree import annotation_to_semantic_tree, is_valid_annotation
from geosolver.text2.model import NaiveTagModel, UnaryModel, NaiveUnaryModel, NaiveBinaryModel, CombinedModel, \
    BinaryModel, NaiveCoreModel, NaiveIsModel, NaiveCCModel
from geosolver.text2.rule import UnaryRule, BinaryRule
from geosolver.text2.semantic_forest import SemanticForest
from geosolver.text2.syntax_parser import SyntaxParse, stanford_parser
import numpy as np
from geosolver.utils.analysis import draw_pr

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
    query = 1014
    questions = geoserver_interface.download_questions(query)
    all_annotations = geoserver_interface.download_semantics(query)
    print "parsing syntax..."
    syntax_parses = {pk: {number: stanford_parser.get_best_syntax_parse(words)
                          for number, words in question.sentence_words.iteritems()}
                     for pk, question in questions.iteritems()}

    all_tag_rules = []

    total = 0
    for pk, question in questions.iteritems():
        for number, sentence_words in question.sentence_words.iteritems():
            syntax_parse = syntax_parses[pk][number]
            semantic_trees = [annotation_to_semantic_tree(syntax_parse, annotation)
                              for annotation in all_annotations[pk][number].values()]
            total += len(semantic_trees)
            tag_rules = itertools.chain(*[semantic_tree.get_tag_rules() for semantic_tree in semantic_trees])
            all_tag_rules.extend(tag_rules)
            # test = NaiveTagModel(all_tag_rules)
    print total

    tag_model = NaiveTagModel(all_tag_rules)

    # tag_model.print_lexicon()

    tree_nums = []
    triples = {th: [0,0,0] for th in np.linspace(0,1,101)} # ref, ret, mat
    for pk, question in questions.iteritems():
        print pk
        for number, sentence_words in question.sentence_words.iteritems():
            syntax_parse = syntax_parses[pk][number]
            true_semantic_trees = set(annotation_to_semantic_tree(syntax_parse, annotation)
                                      for annotation in all_annotations[pk][number].values())
            true_unary_rules = set(itertools.chain(*[semantic_tree.get_unary_rules() for semantic_tree in true_semantic_trees]))
            true_binary_rules = set(itertools.chain(*[semantic_tree.get_binary_rules() for semantic_tree in true_semantic_trees]))
            tag_rules = tag_model.generate_tag_rules(syntax_parse)
            cm = CombinedModel(NaiveUnaryModel(3), NaiveCoreModel(3), NaiveIsModel(3), NaiveCCModel(3))
            unary_rules = [ur for ur in cm.generate_unary_rules(tag_rules)
                           if cm.get_score(ur) > 0]

            binary_rules = [br for br in cm.generate_binary_rules(tag_rules) if cm.get_score(br) > 0]

            for ur in unary_rules:
                print ur
            for br in binary_rules:
                print br
            print ""

            semantic_forest = SemanticForest(tag_rules, unary_rules, binary_rules)
            terminator = lambda tree: False
            core_semantic_trees = semantic_forest.get_semantic_trees_by_type('truth', terminator)
            cc_semantic_trees = semantic_forest.get_semantic_trees_by_type('cc', terminator)
            is_semantic_trees = semantic_forest.get_semantic_trees_by_type("is", terminator)
            all_semantic_trees = set(itertools.chain(core_semantic_trees, cc_semantic_trees, is_semantic_trees))

            semantic_tree_scores = {semantic_tree: cm.get_tree_score(semantic_tree) for semantic_tree in all_semantic_trees}
            missing = true_semantic_trees - all_semantic_trees
            if len(missing) > 0:
                print missing

            ref = len(true_semantic_trees)
            for th, triple in triples.iteritems():
                filtered_semantic_trees = set(semantic_tree for semantic_tree, score in semantic_tree_scores.iteritems()
                                              if score >= th)
                ret = len(filtered_semantic_trees)
                mat = len(true_semantic_trees.intersection(filtered_semantic_trees))
                triple[0] += ref
                triple[1] += ret
                triple[2] += mat

            #sorted_semantic_tree_scores = sorted(semantic_tree_scores.items(), key=lambda pair: -pair[1])


            """
            for semantic_tree, score in sorted_semantic_tree_scores:
                if score < 0.3:
                    break
                print "%.2f: %r, %r" % (score, semantic_tree in true_semantic_trees, semantic_tree)
            """

            tree_nums.append(len(semantic_trees))


            """
            for tag_rule in tag_rules:
                print tag_rule
            """
        print "\n\n"
    print triples
    draw_pr(triples)

    print min(tree_nums), np.mean(tree_nums), max(tree_nums)



if __name__ == "__main__":
    # test_validity()
    test_annotations_to_rules()
