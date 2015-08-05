import itertools
import os
from pprint import pprint
import sys
from geosolver import geoserver_interface
from geosolver.text.annotation_to_semantic_tree import annotation_to_semantic_tree, is_valid_annotation
from geosolver.text.feature_function import UnaryFeatureFunction
from geosolver.text.model import NaiveTagModel, UnaryModel, NaiveUnaryModel, NaiveBinaryModel, CombinedModel, \
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


def train_model(questions, annotations):
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

def evaluate_model(combined_model, questions, annotations, threshold):
    syntax_parses = questions_to_syntax_parses(questions)

    unary_correct = 0
    unary_wrong = 0
    unary_tp, unary_fp, unary_tn, unary_fn = 0, 0, 0, 0
    core_correct = 0
    core_wrong = 0
    core_tp, core_fp, core_tn, core_fn = 0, 0, 0, 0
    is_tp, is_fp, is_tn, is_fn = 0, 0, 0, 0
    is_correct = 0
    is_wrong = 0
    cc_tp, cc_fp, cc_tn, cc_fn = 0, 0, 0, 0
    cc_correct = 0
    cc_wrong = 0
    unary_scores = []
    core_scores = []
    is_scores = []
    cc_scores = []

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

            for pur in positive_unary_rules:
                score = combined_model.get_score(pur)
                unary_scores.append(score)
                if score >= threshold: unary_tp += 1
                else: unary_fn += 1

            for nur in negative_unary_rules:
                score = combined_model.get_score(nur)
                unary_scores.append(1-score)
                if score >= threshold: unary_fp += 1
                else: unary_tn += 1

            for pbr in pos_core_rules:
                score = combined_model.get_score(pbr)
                core_scores.append(score)
                if score >= threshold: core_tp += 1
                else: core_fn += 1

            for nbr in neg_core_rules:
                score = combined_model.get_score(nbr)
                core_scores.append(1-score)
                if score >= threshold: core_fp += 1
                else: core_tn += 1

            for pbr in pos_is_rules:
                score = combined_model.get_score(pbr)
                is_scores.append(score)
                if score >= threshold: is_tp += 1
                else: is_fn += 1

            for nur in neg_is_rules:
                score = combined_model.get_score(nur)
                is_scores.append(1-score)
                if score >= threshold: is_fp += 1
                else: is_tn += 1

            for pbr in pos_cc_rules:
                score = combined_model.get_score(pbr)
                cc_scores.append(score)
                if score >= threshold: cc_tp += 1
                else: cc_fn += 1

            for nbr in neg_cc_rules:
                score = combined_model.get_score(nbr)
                cc_scores.append(1-score)
                if score >= threshold: cc_fp += 1
                else: cc_tn += 1

    #unary_acc = float(unary_correct)/(unary_correct+unary_wrong)
    #core_acc = float(core_correct)/(core_correct+core_wrong)
    # is_acc = float(is_correct)/(is_correct+is_wrong)
    unary_p = float(unary_tp)/(unary_tp+unary_fp)
    unary_r = float(unary_tp)/(unary_tp+unary_fn)
    core_p = float(core_tp)/(core_tp+core_fp)
    core_r = float(core_tp)/(core_tp+core_fn)

    is_p = float(is_tp)/(is_tp+is_fp)
    is_r = float(is_tp)/(is_tp+is_fn)
    cc_p = float(cc_tp)/(cc_tp+cc_fp)
    cc_r = float(cc_tp)/(cc_tp+cc_fn)
    #cc_acc = float(cc_correct)/(cc_correct+cc_wrong)
    """
    print min(unary_scores), np.mean(unary_scores), max(unary_scores), np.std(unary_scores)
    print min(core_scores), np.mean(core_scores), max(core_scores), np.std(core_scores)
    print min(is_scores), np.mean(is_scores), max(is_scores), np.std(is_scores)
    print min(cc_scores), np.mean(cc_scores), max(cc_scores), np.std(cc_scores)
    """
    return (unary_p, unary_r), (core_p, core_r), (is_p, is_r), (cc_p, cc_r)


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
    cm = train_model(tr_q, tr_a)
    result = evaluate_model(cm, te_q, te_a, 0.7)
    print result

if __name__ == "__main__":
    # test_validity()
    # test_annotations_to_rules()
    test_model()
