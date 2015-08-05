import itertools
import os
from pprint import pprint
import sys
from geosolver import geoserver_interface
from geosolver.text2.annotation_to_semantic_tree import annotation_to_semantic_tree, is_valid_annotation
from geosolver.text2.feature_function import UnaryFeatureFunction
from geosolver.text2.model import NaiveTagModel, UnaryModel, NaiveUnaryModel, NaiveBinaryModel, CombinedModel, \
    BinaryModel, NaiveCoreModel, NaiveIsModel, NaiveCCModel, RFUnaryModel
from geosolver.text2.rule import UnaryRule, BinaryRule
from geosolver.text2.semantic_forest import SemanticForest
from geosolver.text2.syntax_parser import SyntaxParse, stanford_parser
import numpy as np
from geosolver.utils.analysis import draw_pr

__author__ = 'minjoon'

def questions_to_syntax_parses(questions):
    syntax_parses = {pk: {number: stanford_parser.get_best_syntax_parse(words)
                          for number, words in question.sentence_words.iteritems()}
                     for pk, question in questions.iteritems()}
    return syntax_parses

def train_model(questions, annotations):
    tm = NaiveTagModel()
    um = RFUnaryModel()
    corem = NaiveBinaryModel(3)
    ism = NaiveIsModel(3)
    ccm = NaiveCCModel(3)

    syntax_parses = questions_to_syntax_parses(questions)
    for pk, local_syntax_parses in syntax_parses.iteritems():
        for number, syntax_parse in local_syntax_parses.iteritems():
            assert isinstance(syntax_parse, SyntaxParse)
            semantic_trees = [annotation_to_semantic_tree(syntax_parse, annotation)
                              for annotation in annotations[pk][number].values()]
            local_tag_rules = set(itertools.chain(*[semantic_tree.get_tag_rules() for semantic_tree in semantic_trees]))
            local_unary_rules = set(itertools.chain(*[semantic_tree.get_unary_rules() for semantic_tree in semantic_trees]))
            local_binary_rules = set(itertools.chain(*[semantic_tree.get_binary_rules() for semantic_tree in semantic_trees]))
            tm.update(local_tag_rules)
            um.update(local_tag_rules, local_unary_rules)

    um.fit()

    cm = CombinedModel(tm, um, corem, ism, ccm)
    return cm

def evaluate_model(combined_model, questions, annotations):
    syntax_parses = questions_to_syntax_parses(questions)

    unary_correct = 0
    unary_wrong = 0

    for pk, local_syntax_parses in syntax_parses.iteritems():
        for number, syntax_parse in local_syntax_parses.iteritems():
            semantic_trees = [annotation_to_semantic_tree(syntax_parse, annotation)
                              for annotation in annotations[pk][number].values()]
            positive_tag_rules = set(itertools.chain(*[semantic_tree.get_tag_rules() for semantic_tree in semantic_trees]))
            positive_unary_rules = set(itertools.chain(*[semantic_tree.get_unary_rules() for semantic_tree in semantic_trees]))
            positive_binary_rules = set(itertools.chain(*[semantic_tree.get_binary_rules() for semantic_tree in semantic_trees]))

            negative_unary_rules = combined_model.generate_unary_rules(positive_tag_rules) - positive_unary_rules

            for pur in positive_unary_rules:
                score = combined_model.get_score(pur)
                if score >= 0.5: unary_correct += 1
                else: unary_wrong += 1

            for nur in negative_unary_rules:
                score = combined_model.get_score(nur)
                if score >= 0.5: unary_wrong += 1
                else: unary_correct += 1

    unary_acc = float(unary_correct)/(unary_correct+unary_wrong)
    return unary_acc


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
    result = evaluate_model(cm, te_q, te_a)
    print result






def test_annotations_to_rules():
    query = 'test'
    questions = geoserver_interface.download_questions(query)
    all_annotations = geoserver_interface.download_semantics(query)
    print "parsing syntax..."
    syntax_parses = {pk: {number: stanford_parser.get_best_syntax_parse(words)
                          for number, words in question.sentence_words.iteritems()}
                     for pk, question in questions.iteritems()}

    # Training
    positive_tag_rules = []
    positive_unary_rules = []
    negative_unary_rules = []
    positive_binary_rules = []
    distances = []

    um = RFUnaryModel()

    for pk, local_syntax_parses in syntax_parses.iteritems():
        for number, syntax_parse in local_syntax_parses.iteritems():
            assert isinstance(syntax_parse, SyntaxParse)
            semantic_trees = [annotation_to_semantic_tree(syntax_parse, annotation)
                              for annotation in all_annotations[pk][number].values()]
            tag_rules = set(itertools.chain(*[semantic_tree.get_tag_rules() for semantic_tree in semantic_trees]))
            unary_rules = set(itertools.chain(*[semantic_tree.get_unary_rules() for semantic_tree in semantic_trees]))
            binary_rules = set(itertools.chain(*[semantic_tree.get_binary_rules() for semantic_tree in semantic_trees]))
            positive_tag_rules.extend(tag_rules)
            positive_unary_rules.extend(unary_rules)
            positive_binary_rules.extend(binary_rules)
            local_negative_unary_rules = um.generate_unary_rules(tag_rules) - unary_rules
            negative_unary_rules.extend(local_negative_unary_rules)

            """
            for binary_rule in binary_rules:
                assert isinstance(binary_rule, BinaryRule)
                d0 = binary_rule.syntax_parse.distance_between_spans(binary_rule.parent_tag_rule.span, binary_rule.child_a_tag_rule.span)
                d1 = binary_rule.syntax_parse.distance_between_spans(binary_rule.parent_tag_rule.span, binary_rule.child_b_tag_rule.span)
                d2 = binary_rule.syntax_parse.distance_between_spans(binary_rule.child_a_tag_rule.span, binary_rule.child_b_tag_rule.span)
                if min(d0, d1, d2) > 1:
                    print pk, number, d0, d1, d2, binary_rule
                distances.extend([d0,d1,d2])
            """
            um.update(unary_rules, local_negative_unary_rules)

    um.fit()
    for unary_rule in positive_unary_rules:
        print "%.3f: %r" % (um.predict_proba(unary_rule), unary_rule)
    print ""
    for unary_rule in negative_unary_rules:
        print "%.3f: %r" % (um.predict_proba(unary_rule), unary_rule)

    # print len(distances), min(distances), np.mean(distances), max(distances)

    tag_model = NaiveTagModel(positive_tag_rules)
    cm = CombinedModel(NaiveUnaryModel(3), NaiveCoreModel(3), NaiveIsModel(3), NaiveCCModel(3))

    # tag_model.print_lexicon()



    # Testing
    tree_nums = []
    triples = {th: [0,0,0] for th in np.linspace(0,1,101)} # ref, ret, mat
    rule_triples = {th: [0,0,0] for th in np.linspace(0,1,101)} # ref, ret, mat
    for pk, local_syntax_parses in syntax_parses.iteritems():
        print pk
        for number, syntax_parse in local_syntax_parses.iteritems():
            true_semantic_trees = set(annotation_to_semantic_tree(syntax_parse, annotation)
                                      for annotation in all_annotations[pk][number].values())
            true_cc_semantic_trees = set(t for t in true_semantic_trees if t.content.signature.id == "CC")
            true_is_semantic_trees = set(t for t in true_semantic_trees if t.content.signature.id == "Is")
            positive_unary_rules = set(itertools.chain(*[semantic_tree.get_unary_rules() for semantic_tree in true_semantic_trees]))
            positive_binary_rules = set(itertools.chain(*[semantic_tree.get_binary_rules() for semantic_tree in true_semantic_trees]))
            positive_is_rules = set(t for t in positive_binary_rules if t.parent_tag_rule.signature.id == 'Is')
            tag_rules = tag_model.generate_tag_rules(syntax_parse)
            unary_rules = set(ur for ur in cm.generate_unary_rules(tag_rules)
                           if cm.get_score(ur) > 0)

            binary_rules = set(br for br in cm.generate_binary_rules(tag_rules) if cm.get_score(br) > 0)
            is_rules = set(br for br in binary_rules if br.parent_tag_rule.signature.id == 'Is')

            """
            print "tag rules:", tag_rules
            for ur in unary_rules:
                print ur
            for br in binary_rules:
                print br
            """

            semantic_forest = SemanticForest(tag_rules, unary_rules, binary_rules)
            terminator = lambda tree: False
            core_semantic_trees = semantic_forest.get_semantic_trees_by_type('truth', terminator)
            cc_semantic_trees = semantic_forest.get_semantic_trees_by_type('cc', terminator)
            is_semantic_trees = semantic_forest.get_semantic_trees_by_type("is", terminator)
            all_semantic_trees = set(itertools.chain(core_semantic_trees, cc_semantic_trees, is_semantic_trees))


            binary_rules = is_rules
            positive_binary_rules = positive_is_rules

            semantic_tree_scores = {semantic_tree: cm.get_tree_score(semantic_tree) for semantic_tree in all_semantic_trees}
            binary_rule_scores = {br: cm.get_score(br) for br in binary_rules}
            missing = true_semantic_trees - all_semantic_trees
            # fp = all_semantic_trees - true_semantic_trees
            if len(missing) > 0:
                for br in missing:
                    print "missing:", br

            fp = binary_rules - positive_binary_rules
            for br in fp:
                print "fp: %r" % (br)
            print ""


            for th, triple in triples.iteritems():
                filtered_semantic_trees = set(semantic_tree for semantic_tree, score in semantic_tree_scores.iteritems()
                                              if score >= th)
                triple[0] += len(true_semantic_trees)
                triple[1] += len(filtered_semantic_trees)
                triple[2] += len(true_semantic_trees.intersection(filtered_semantic_trees))

            for th, rule_triple in rule_triples.iteritems():
                filtered_binary_rules = set(br for br, score in binary_rule_scores.iteritems() if score >= th)
                rule_triple[0] += len(positive_binary_rules)
                rule_triple[1] += len(filtered_binary_rules)
                rule_triple[2] += len(positive_binary_rules.intersection(filtered_binary_rules))

            #sorted_semantic_tree_scores = sorted(semantic_tree_scores.items(), key=lambda pair: -pair[1])


            """
            for semantic_tree, score in sorted_semantic_tree_scores:
                if score < 0.3:
                    break
                print "%.2f: %r, %r" % (score, semantic_tree in true_semantic_trees, semantic_tree)
            """

            tree_nums.append(len(all_semantic_trees))


            """
            for tag_rule in tag_rules:
                print tag_rule
            """
        print "\n\n"
    # draw_pr(triples)
    draw_pr(rule_triples)

    print min(tree_nums), np.mean(tree_nums), max(tree_nums)



if __name__ == "__main__":
    # test_validity()
    # test_annotations_to_rules()
    test_model()
