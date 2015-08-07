from collections import defaultdict
import itertools
import os
from pprint import pprint
import sys
from geosolver import geoserver_interface
from geosolver.text.annotation_to_semantic_tree import annotation_to_semantic_tree, is_valid_annotation
from geosolver.text.feature_function import UnaryFeatureFunction
from geosolver.text.opt_model import GreedyOptModel, TextGreedyOptModel
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
    syntax_parses = questions_to_syntax_parses(questions)
    tm = NaiveTagModel()

    for pk, local_syntax_parses in syntax_parses.iteritems():
        for number, syntax_parse in local_syntax_parses.iteritems():
            semantic_trees = [annotation_to_semantic_tree(syntax_parse, annotation)
                              for annotation in annotations[pk][number].values()]
            assert isinstance(syntax_parse, SyntaxParse)
            local_tag_rules = set(itertools.chain(*[semantic_tree.get_tag_rules() for semantic_tree in semantic_trees]))
            tm.update(local_tag_rules)

    um = RFUnaryModel()
    corem = RFCoreModel()
    ism = RFIsModel()
    ccm = RFCCModel()

    for pk, local_syntax_parses in syntax_parses.iteritems():
        for number, syntax_parse in local_syntax_parses.iteritems():
            assert isinstance(syntax_parse, SyntaxParse)
            semantic_trees = [annotation_to_semantic_tree(syntax_parse, annotation)
                              for annotation in annotations[pk][number].values()]
            local_tag_rules = tm.generate_tag_rules(syntax_parse)
            local_unary_rules = set(itertools.chain(*[semantic_tree.get_unary_rules() for semantic_tree in semantic_trees]))
            local_binary_rules = set(itertools.chain(*[semantic_tree.get_binary_rules() for semantic_tree in semantic_trees]))
            core_rules, is_rules, cc_rules = split_binary_rules(local_binary_rules)

            # Sanity check
            for ur in local_unary_rules:
                assert um.val_func(ur.parent_tag_rule, ur.child_tag_rule)
            for br in core_rules:
                assert corem.val_func(br.parent_tag_rule, br.child_a_tag_rule, br.child_b_tag_rule)

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

    all_pos_semantic_trees = []
    all_neg_semantic_trees = []

    for pk, local_syntax_parses in syntax_parses.iteritems():
        print "\n\n\n"
        print pk
        for number, syntax_parse in local_syntax_parses.iteritems():
            pos_semantic_trees = set(annotation_to_semantic_tree(syntax_parse, annotation)
                                     for annotation in annotations[pk][number].values())

            pos_unary_rules = set(itertools.chain(*[semantic_tree.get_unary_rules() for semantic_tree in pos_semantic_trees]))
            pos_binary_rules = set(itertools.chain(*[semantic_tree.get_binary_rules() for semantic_tree in pos_semantic_trees]))

            tag_rules = combined_model.generate_tag_rules(syntax_parse)

            unary_rules = combined_model.generate_unary_rules(tag_rules)
            binary_rules = combined_model.generate_binary_rules(tag_rules)
            core_rules = combined_model.core_model.generate_binary_rules(tag_rules)
            is_rules = combined_model.is_model.generate_binary_rules(tag_rules)
            cc_rules = combined_model.cc_model.generate_binary_rules(tag_rules)
            pos_core_rules, pos_is_rules, pos_cc_rules = split_binary_rules(pos_binary_rules)
            negative_unary_rules = unary_rules - pos_unary_rules
            neg_core_rules = core_rules - pos_core_rules
            neg_is_rules = is_rules - pos_is_rules
            neg_cc_rules = cc_rules - pos_cc_rules

            all_pos_unary_rules.extend(pos_unary_rules)
            all_pos_core_rules.extend(pos_core_rules)
            all_pos_is_rules.extend(pos_is_rules)
            all_pos_cc_rules.extend(pos_cc_rules)
            all_neg_unary_rules.extend(negative_unary_rules)
            all_neg_core_rules.extend(neg_core_rules)
            all_neg_is_rules.extend(neg_is_rules)
            all_neg_cc_rules.extend(neg_cc_rules)

            semantic_forest = SemanticForest(tag_rules, unary_rules, binary_rules)
            semantic_trees = semantic_forest.get_semantic_trees_by_type("truth").union(semantic_forest.get_semantic_trees_by_type('is'))
            neg_semantic_trees = semantic_trees - pos_semantic_trees
            all_pos_semantic_trees.extend(pos_semantic_trees)
            all_neg_semantic_trees.extend(neg_semantic_trees)

            for pst in pos_semantic_trees:
                print "pos:", combined_model.get_tree_score(pst), pst
            print ""
            for nst in neg_semantic_trees:
                print "neg:", combined_model.get_tree_score(nst), nst

    unary_prs = combined_model.unary_model.get_prs(all_pos_unary_rules, all_neg_unary_rules, thresholds)
    core_prs = combined_model.core_model.get_prs(all_pos_core_rules, all_neg_core_rules, thresholds)
    is_prs = combined_model.is_model.get_prs(all_pos_is_rules, all_neg_is_rules, thresholds)
    cc_prs = combined_model.cc_model.get_prs(all_pos_cc_rules, all_neg_cc_rules, thresholds)
    core_tree_prs = combined_model.get_tree_prs(all_pos_semantic_trees, all_neg_semantic_trees, thresholds)

    return unary_prs, core_prs, is_prs, cc_prs, core_tree_prs


def evaluate_opt_model(opt_model, questions, annotations, thresholds):
    assert isinstance(opt_model, GreedyOptModel)
    syntax_parses = questions_to_syntax_parses(questions)

    combined_model = opt_model.combined_model

    tps, fps, tns, fns = defaultdict(int), defaultdict(int), defaultdict(int), defaultdict(int)

    for pk, local_syntax_parses in syntax_parses.iteritems():
        print pk
        for number, syntax_parse in local_syntax_parses.iteritems():
            pos_semantic_trees = set(annotation_to_semantic_tree(syntax_parse, annotation)
                                     for annotation in annotations[pk][number].values())
            tag_rules = combined_model.generate_tag_rules(syntax_parse)
            unary_rules = combined_model.generate_unary_rules(tag_rules)
            binary_rules = combined_model.generate_binary_rules(tag_rules)

            semantic_forest = SemanticForest(tag_rules, unary_rules, binary_rules)
            semantic_trees = semantic_forest.get_semantic_trees_by_type("truth").union(semantic_forest.get_semantic_trees_by_type('is'))
            semantic_trees = set(t for t in semantic_trees if combined_model.get_tree_score(t) > 0.01)
            neg_semantic_trees = semantic_trees - pos_semantic_trees

            for th in thresholds:
                selected_trees = opt_model.optimize(semantic_trees, th)
                tp = len(selected_trees - neg_semantic_trees)
                fp = len(selected_trees - pos_semantic_trees)
                tn = len(neg_semantic_trees - selected_trees)
                fn = len(pos_semantic_trees - selected_trees)
                tps[th] += tp
                fps[th] += fp
                tns[th] += tn
                fns[th] += fn

    prs = {}

    for th in thresholds:
        p = float(tps[th])/(tps[th]+fps[th])
        r = float(tps[th])/(tps[th]+fns[th])
        prs[th] = p, r

    return prs

def split(questions, annotations, mid, end=1):
    keys = questions.keys()
    bk = int(mid*len(keys))
    ep = int(end*len(keys))
    left_keys = keys[:bk]
    right_keys = keys[bk:ep]
    left_questions = {pk: questions[pk] for pk in left_keys}
    right_questions = {pk: questions[pk] for pk in right_keys}
    left_annotations = {pk: annotations[pk] for pk in left_keys}
    right_annotations = {pk: annotations[pk] for pk in right_keys}

    return (left_questions, left_annotations), (right_questions, right_annotations)


def test_rule_model():
    query = 'test'
    all_questions = geoserver_interface.download_questions(query)
    all_annotations = geoserver_interface.download_semantics(query)

    (te_q, te_a), (tr_q, tr_a) = split(all_questions, all_annotations, 0.5)
    cm = train_rule_model(tr_q, tr_a)
    unary_prs, core_prs, is_prs, cc_prs, core_tree_prs = evaluate_rule_model(cm, te_q, te_a, np.linspace(0,1,101))

    plt.plot(core_tree_prs.keys(), core_tree_prs.values(), 'o')
    plt.show()
    plt.plot(unary_prs.keys(), unary_prs.values(), 'o')
    plt.show()
    plt.plot(core_prs.keys(), core_prs.values(), 'o')
    plt.show()
    plt.plot(is_prs.keys(), is_prs.values(), 'o')
    plt.show()
    plt.plot(cc_prs.keys(), cc_prs.values(), 'o')
    plt.show()

def test_opt_model():
    query = 'test'
    all_questions = geoserver_interface.download_questions(query)
    all_annotations = geoserver_interface.download_semantics(query)

    (te_q, te_a), (tr_q, tr_a) = split(all_questions, all_annotations, 0.5)
    cm = train_rule_model(tr_q, tr_a)
    om = TextGreedyOptModel(cm)
    prs = evaluate_opt_model(om, te_q, te_a, np.linspace(-2,2,21))
    ps, rs = zip(*prs.values())
    plt.plot(prs.keys(), ps, 'o', label='precision')
    plt.plot(prs.keys(), rs, 'o', label='recall')
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
    plt.show()


if __name__ == "__main__":
    # test_rule_model()
    test_opt_model()
