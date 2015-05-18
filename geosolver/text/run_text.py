import timeit
import numpy as np
from geosolver.database.geoserver_interface import geoserver_interface
from geosolver.text.annotation_to_node import annotation_to_node, is_valid_annotation
from geosolver.text.decoder import TopDownLiftedDecoder
from geosolver.text.dependency_parser import stanford_parser
from geosolver.text.feature_function import generate_unary_feature_function, generate_binary_feature_function
from geosolver.text.semantic_model_2 import UnarySemanticModel
from geosolver.text.semantic_model_2 import BinarySemanticModel
from geosolver.text.tag_model import CountBasedTagModel
from geosolver.text.transitions import node_to_semantic_rules, tag_rules_to_tags, rules_to_impliable_signatures
from geosolver.text.transitions import node_to_tag_rules
import matplotlib.pyplot as plt
import cPickle as pickle
from dist_utils import normalize

__author__ = 'minjoon'

def replace(words):
    new_words = {}
    for index, word in words.iteritems():
        if word == "=":
            new_words[index] = 'equals'
        elif word == "+":
            new_words[index] = 'plus'
        else:
            new_words[index] = word
    return new_words

def get_models():
    query = "annotated"
    print "Obtaining questions and semantic annotations..."
    questions = geoserver_interface.download_questions([query])
    semantics = geoserver_interface.download_semantics([query])

    print "Obtaining syntax trees..."
    if False:
        syntax_trees = {pk: {sentence_index: stanford_parser.get_best_syntax_tree(replace(words))
                             for sentence_index, words in question.words.iteritems()}
                        for pk, question in questions.iteritems()}
        pickle.dump(syntax_trees, open("syntax_trees.p", 'wb'))
    else:
        syntax_trees = pickle.load(open("syntax_trees.p", 'rb'))

    print "Obtaining nodes..."
    nodes = {pk: {sentence_index: [annotation_to_node(annotation) for _, annotation in annotations.iteritems()]
                  for sentence_index, annotations in d.iteritems()}
             for pk, d in semantics.iteritems()}

    print "Extracting tag rules..."
    tag_rules = []
    for pk, d in nodes.iteritems():
        for sentence_index, dd in d.iteritems():
            syntax_tree = syntax_trees[pk][sentence_index]
            for node in dd:
                local_tag_rules = node_to_tag_rules(syntax_tree.words, syntax_tree, node)
                tag_rules.extend(local_tag_rules)

    print "Learning tag model..."
    tag_model = CountBasedTagModel(tag_rules)

    print "Extracting semantic rules..."
    unary_rules = []
    binary_rules = []
    for pk, d in nodes.iteritems():
        for sentence_index, dd in d.iteritems():
            syntax_tree = syntax_trees[pk][sentence_index]
            for node in dd:
                local_unary_rules, local_binary_rules = node_to_semantic_rules(syntax_tree.words, syntax_tree, tag_model, node, lift_index=True)
                unary_rules.extend(local_unary_rules)
                binary_rules.extend(local_binary_rules)

    # localities = {function_signatures['add']: 1}
    impliable_signatures = rules_to_impliable_signatures(unary_rules + binary_rules)
    uff1 = generate_unary_feature_function(unary_rules)
    bff1 = generate_binary_feature_function(binary_rules)
    print "Learning unary model..."
    unary_model = UnarySemanticModel(uff1, impliable_signatures=impliable_signatures)
    unary_model.fit(unary_rules, 1)
    print "Learning binary model..."
    binary_model = BinarySemanticModel(bff1, impliable_signatures=impliable_signatures)
    binary_model.fit(binary_rules, 1)

    print "unary weights:", unary_model.weights
    print "binary_weights:", binary_model.weights
    print "impliable:", unary_model.impliable_signatures, binary_model.impliable_signatures

    return tag_model, unary_model, binary_model



def test_models(tag_model, unary_model, binary_model):
    print("Testing the model...")
    query = "annotated"
    questions = geoserver_interface.download_questions([query])
    semantics = geoserver_interface.download_semantics([query])
    all_gt_nodes = {}
    all_my_node_dict = {}
    reweighed_my_dict = {}

    sizes = []

    for pk, question in questions.iteritems():
        all_gt_nodes[pk] = {}
        all_my_node_dict[pk] = {}
        reweighed_my_dict[pk] = {}
        for sentence_index, words in question.words.iteritems():
            all_gt_nodes[pk][sentence_index] = set(annotation_to_node(annotation) for annotation in semantics[pk][sentence_index].values())
            all_my_node_dict[pk][sentence_index] = {}
            reweighed_my_dict[pk][sentence_index] = {}
            words = replace(words)
            syntax_tree = stanford_parser.get_best_syntax_tree(words)
            decoder = TopDownLiftedDecoder(unary_model, binary_model)
            dist = decoder.get_formula_distribution(words, syntax_tree, tag_model)
            items = sorted(dist.items(), key=lambda x: x[1])
            sizes.append(len(items))
            print "---------------"
            print pk, sentence_index
            print " ".join(words.values())
            for node, logp in items:
                # print(node_to_semantic_rules(words, syntax_tree, tags, node, True))
                print node, np.exp(logp)
                all_my_node_dict[pk][sentence_index][node] = np.exp(logp)
            reweighed_my_dict[pk][sentence_index] = reweigh(words, syntax_tree, tag_model, all_my_node_dict[pk][sentence_index])

    print "--------------"
    print "sizes:", max(sizes), np.median(sizes), min(sizes)


    #prs =  [get_pr(all_gt_nodes, all_my_node_dict, conf) for conf in np.linspace(-0.1,1.1,121)]
    prs =  [get_pr_by_rank(all_gt_nodes, all_my_node_dict, rank) for rank in range(1,400)]
    print prs
    #re_prs =  [get_pr(all_gt_nodes, reweighed_my_dict, conf) for conf in np.linspace(-0.1,1.1,121)]
    re_prs =  [get_pr_by_rank(all_gt_nodes, reweighed_my_dict, rank) for rank in range(1,400)]
    draw(prs)
    draw(re_prs)
    plt.show()
    pr = get_pr(all_gt_nodes, all_my_node_dict, 0)


def draw(prs):
    ps, rs = zip(*prs)
    plt.plot(rs, ps)


def get_pr_by_rank(all_gt_nodes, all_my_node_dict, rank):
    retrieved = 0
    relevant = 0
    intersection = 0

    for pk, question in all_gt_nodes.iteritems():
        for index, curr_gt_nodes in question.iteritems():
            curr_my_node_dict = all_my_node_dict[pk][index]
            my_nodes = set([y[0] for y in sorted(curr_my_node_dict.items(), key=lambda x: -x[1])][:rank])
            intersection_set = curr_gt_nodes.intersection(my_nodes)
            retrieved += len(my_nodes)
            relevant += len(curr_gt_nodes)
            intersection += len(intersection_set)
            """
            if len(intersection_set) < len(curr_gt_nodes):
                print curr_gt_nodes-intersection_set
            """

    if retrieved == 0:
        precision = 1
    else:
        precision = float(intersection)/retrieved
    recall = float(intersection)/relevant
    # print missed_set

    return precision, recall


def get_pr(all_gt_nodes, all_my_node_dict, threshold):
    retrieved = 0
    relevant = 0
    intersection = 0

    for pk, question in all_gt_nodes.iteritems():
        for index, curr_gt_nodes in question.iteritems():
            curr_my_node_dict = all_my_node_dict[pk][index]
            my_nodes = set(node for node, prob in curr_my_node_dict.iteritems() if prob >= threshold)
            intersection_set = curr_gt_nodes.intersection(my_nodes)
            retrieved += len(my_nodes)
            relevant += len(curr_gt_nodes)
            intersection += len(intersection_set)
            """
            if len(intersection_set) < len(curr_gt_nodes):
                print curr_gt_nodes-intersection_set
            """

    if retrieved == 0:
        precision = 1
    else:
        precision = float(intersection)/retrieved
    recall = float(intersection)/relevant
    # print missed_set

    return precision, recall


def get_coverage(words, syntax_tree, tag_model, nodes):
    all_indices = set()
    for index, word in words.iteritems():
        dist = tag_model.get_log_distribution(word)
        if None not in dist or dist[None] < 0:
            all_indices.add(index)

    covered_indices = set()
    for node in nodes:
        tag_rules = node_to_tag_rules(words, syntax_tree, node)
        current_covered_indices = set([tag_rule.index for tag_rule in tag_rules if tag_rule.index is not None])
        covered_indices = covered_indices.union(current_covered_indices)
    return float(len(covered_indices))/len(all_indices)


def reweigh(words, syntax_tree, tags, node_dict):
    new_dict = {}
    for node, prob in node_dict.iteritems():
        coverage = get_coverage(words, syntax_tree, tags, [node])
        new_dict[node] = prob * coverage

    if sum(new_dict.values()) == 0:
        return new_dict

    return normalize(new_dict)



def get_node_sequence(words, syntax_tree, tags, nodes):
    sequence = []



def is_valid_node(node):
    """
    1. no constant is used twice
    2.
    :param node:
    :return:
    """







if __name__ == "__main__":
    tag_model, unary_model, binary_model = get_models()
    test_models(tag_model, unary_model, binary_model)