import itertools
import os
from pprint import pprint
import sys
from geosolver import geoserver_interface
from geosolver.text.annotation_to_semantic_tree import annotation_to_semantic_tree, is_valid_annotation
from geosolver.text.feature_function import UnaryFeatureFunction
from geosolver.text.rule_model import NaiveTagModel, UnaryModel, NaiveUnaryModel, NaiveBinaryModel, CombinedModel, \
    BinaryModel, NaiveCoreModel, NaiveIsModel, NaiveCCModel, RFUnaryModel, RFCoreModel, RFIsModel, RFCCModel
from geosolver.text.rule import UnaryRule, BinaryRule
from geosolver.text.semantic_forest import SemanticForest
from geosolver.text.syntax_parser import SyntaxParse, stanford_parser
import numpy as np
from geosolver.utils.analysis import draw_pr
import matplotlib.pyplot as plt

__author__ = 'minjoon'

def questions_to_syntax_parses(questions):
    syntax_parses = {pk: {number: stanford_parser.get_best_syntax_parse(words)
                          for number, words in question.sentence_words.iteritems()}
                     for pk, question in questions.iteritems()}
    return syntax_parses

def split_binary_rules(binary_rules):
    core_rules = set()
    is_rules = set()
    cc_rules = set()
    for br in binary_rules:
        id_ = br.parent_tag_rule.signature.id
        if id_ == "Is":
            is_rules.add(br)
        elif id_ == "CC":
            cc_rules.add(br)
        else:
            core_rules.add(br)
    return core_rules, is_rules, cc_rules


def train_rule_model(questions, annotations):
    tm = NaiveTagModel()
    um = RFUnaryModel()
    corem = RFCoreModel()
    ism = RFIsModel()
    ccm = RFCCModel()

    syntax_parses = questions_to_syntax_parses(questions)
    for pk, local_syntax_parses in syntax_parses.iteritems():
        for number, syntax_parse in local_syntax_parses.iteritems():
            assert isinstance(syntax_parse, SyntaxParse)
            semantic_trees = [annotation_to_semantic_tree(syntax_parse, annotation)
                              for annotation in annotations[pk][number].values()]
            local_tag_rules = set(itertools.chain(*[semantic_tree.get_tag_rules() for semantic_tree in semantic_trees]))
            local_unary_rules = set(itertools.chain(*[semantic_tree.get_unary_rules() for semantic_tree in semantic_trees]))
            local_binary_rules = set(itertools.chain(*[semantic_tree.get_binary_rules() for semantic_tree in semantic_trees]))
            core_rules, is_rules, cc_rules = split_binary_rules(local_binary_rules)

            # Sanity check
            for ur in local_unary_rules:
                assert um.val_func(ur.parent_tag_rule, ur.child_tag_rule)
            for br in core_rules:
                assert corem.val_func(br.parent_tag_rule, br.child_a_tag_rule, br.child_b_tag_rule)

            tm.update(local_tag_rules)
            um.update(local_tag_rules, local_unary_rules)
            corem.update(local_tag_rules, core_rules)
            ism.update(local_tag_rules, is_rules)
            ccm.update(local_tag_rules, cc_rules)

    um.fit()
    corem.fit()
    ism.fit()
    ccm.fit()

    cm = CombinedModel(tm, um, corem, ism, ccm)
    return cm

def evaluate_rule_model(combined_model, questions, annotations, thresholds):
    syntax_parses = questions_to_syntax_parses(questions)

    all_pos_unary_rules = []
    all_pos_core_rules = []
    all_pos_is_rules = []
    all_pos_cc_rules = []
    all_neg_unary_rules = []
    all_neg_core_rules = []
    all_neg_is_rules = []
    all_neg_cc_rules = []

    for pk, local_syntax_parses in syntax_parses.iteritems():
        for number, syntax_parse in local_syntax_parses.iteritems():
            semantic_trees = [annotation_to_semantic_tree(syntax_parse, annotation)
                              for annotation in annotations[pk][number].values()]
            positive_tag_rules = set(itertools.chain(*[semantic_tree.get_tag_rules() for semantic_tree in semantic_trees]))
            positive_unary_rules = set(itertools.chain(*[semantic_tree.get_unary_rules() for semantic_tree in semantic_trees]))
            positive_binary_rules = set(itertools.chain(*[semantic_tree.get_binary_rules() for semantic_tree in semantic_trees]))
            pos_core_rules, pos_is_rules, pos_cc_rules = split_binary_rules(positive_binary_rules)

            negative_unary_rules = combined_model.generate_unary_rules(positive_tag_rules) - positive_unary_rules
            neg_core_rules = combined_model.core_model.generate_binary_rules(positive_tag_rules) - pos_core_rules
            neg_is_rules = combined_model.is_model.generate_binary_rules(positive_tag_rules) - pos_is_rules
            neg_cc_rules = combined_model.cc_model.generate_binary_rules(positive_tag_rules) - pos_cc_rules

            all_pos_unary_rules.extend(positive_unary_rules)
            all_pos_core_rules.extend(pos_core_rules)
            all_pos_is_rules.extend(pos_is_rules)
            all_pos_cc_rules.extend(pos_cc_rules)
            all_neg_unary_rules.extend(negative_unary_rules)
            all_neg_core_rules.extend(neg_core_rules)
            all_neg_is_rules.extend(neg_is_rules)
            all_neg_cc_rules.extend(neg_cc_rules)

    unary_prs = combined_model.unary_model.get_prs(all_pos_unary_rules, all_neg_unary_rules, thresholds)
    core_prs = combined_model.core_model.get_prs(all_pos_core_rules, all_neg_core_rules, thresholds)
    is_prs = combined_model.is_model.get_prs(all_pos_is_rules, all_neg_is_rules, thresholds)
    cc_prs = combined_model.cc_model.get_prs(all_pos_cc_rules, all_neg_cc_rules, thresholds)

    return unary_prs, core_prs, is_prs, cc_prs



def split(questions, annotations, ratio):
    keys = questions.keys()
    bk = int(ratio*len(keys))
    left_keys = keys[:bk]
    right_keys = keys[bk:]
    left_questions = {pk: questions[pk] for pk in left_keys}
    right_questions = {pk: questions[pk] for pk in right_keys}
    left_annotations = {pk: annotations[pk] for pk in left_keys}
    right_annotations = {pk: annotations[pk] for pk in right_keys}

    return (left_questions, left_annotations), (right_questions, right_annotations)


def test_model():
    query = 'test'
    all_questions = geoserver_interface.download_questions(query)
    all_annotations = geoserver_interface.download_semantics(query)

    (te_q, te_a), (tr_q, tr_a) = split(all_questions, all_annotations, 0.5)
    cm = train_rule_model(tr_q, tr_a)
    unary_prs, core_prs, is_prs, cc_prs = evaluate_rule_model(cm, te_q, te_a, np.linspace(0,1,101))

    plt.plot(unary_prs.keys(), unary_prs.values(), 'o')
    plt.show()
    plt.plot(core_prs.keys(), core_prs.values(), 'o')
    plt.show()
    plt.plot(is_prs.keys(), is_prs.values(), 'o')
    plt.show()
    plt.plot(cc_prs.keys(), cc_prs.values(), 'o')
    plt.show()

if __name__ == "__main__":
    # test_validity()
    # test_annotations_to_rules()
    test_model()
