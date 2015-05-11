import numpy as np
from geosolver.database.geoserver_interface import geoserver_interface
from geosolver.text.annotation_to_node import annotation_to_node, is_valid_annotation
from geosolver.text.decoder import TopDownLiftedDecoder
from geosolver.text.dependency_parser import stanford_parser
from geosolver.text.feature_function import UFF1, UFF2
from geosolver.text.feature_function import BFF1
from geosolver.text.semantic_model_2 import UnarySemanticModel
from geosolver.text.semantic_model_2 import BinarySemanticModel
from geosolver.text.tag_model import CountBasedTagModel
from geosolver.text.transitions import node_to_semantic_rules, tag_rules_to_tags
from geosolver.text.transitions import node_to_tag_rules
import matplotlib.pyplot as plt

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
    questions = geoserver_interface.download_questions([query])
    semantics = geoserver_interface.download_semantics([query])

    tag_rules = []
    unary_rules = []
    binary_rules = []
    for pk, question in questions.iteritems():
        for sentence_index, words in question.words.iteritems():
            words = replace(words)
            syntax_tree = stanford_parser.get_best_syntax_tree(words)
            # display_graph(syntax_tree.directed)
            annotations = semantics[pk][sentence_index]
            sentence_tag_rules = []
            for num, annotation in annotations.iteritems():
                if not is_valid_annotation(annotation):
                    raise Exception("%d %d %d %s" % (pk, sentence_index, num, annotation))
                node = annotation_to_node(annotation)
                local_tag_rules = node_to_tag_rules(words, syntax_tree, node)
                sentence_tag_rules.extend(local_tag_rules)
                tag_rules.extend(local_tag_rules)
            tags = tag_rules_to_tags(words, sentence_tag_rules)

            for num, annotation in annotations.iteritems():
                node = annotation_to_node(annotation)
                local_unary_rules, local_binary_rules = node_to_semantic_rules(words, syntax_tree, tags, node, lift_index=True)
                unary_rules.extend(local_unary_rules)
                binary_rules.extend(local_binary_rules)

    tag_model = CountBasedTagModel(tag_rules)

    # localities = {function_signatures['add']: 1}
    unary_model = UnarySemanticModel(UFF2())
    print("Learning unary model...")
    unary_model.fit(unary_rules, 1)
    binary_model = BinarySemanticModel(BFF1())
    print("Learning binary model...")
    binary_model.fit(binary_rules, 1)

    print unary_model.weights
    print binary_model.weights

    return tag_model, unary_model, binary_model



def test_models(tag_model, unary_model, binary_model):
    print("Testing the model...")
    query = "annotated"
    questions = geoserver_interface.download_questions([query])
    semantics = geoserver_interface.download_semantics([query])
    all_gt_nodes = {}
    all_my_node_dict = {}
    reweighed_my_dict = {}

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
            tags = tag_model.get_best_tags(words, syntax_tree)
            decoder = TopDownLiftedDecoder(unary_model, binary_model)
            dist = decoder.get_formula_distribution(words, syntax_tree, tags)
            items = sorted(dist.items(), key=lambda x: x[1])
            print "---------------"
            print pk, sentence_index
            print " ".join(words.values())
            for node, logp in items:
                # print(node_to_semantic_rules(words, syntax_tree, tags, node, True))
                print node, np.exp(logp)
                all_my_node_dict[pk][sentence_index][node] = np.exp(logp)
            reweighed_my_dict[pk][sentence_index] = reweigh(words, syntax_tree, tags, all_my_node_dict[pk][sentence_index])

    prs =  [get_pr(all_gt_nodes, all_my_node_dict, conf) for conf in np.linspace(0,1,101)]
    re_prs =  [get_pr(all_gt_nodes, reweighed_my_dict, conf) for conf in np.linspace(0,1,101)]
    draw(prs)
    draw(re_prs)
    plt.show()


def draw(prs):
    ps, rs = zip(*prs)
    plt.plot(rs, ps)




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

    if retrieved == 0:
        precision = 1
    else:
        precision = float(intersection)/retrieved
    recall = float(intersection)/relevant
    # print missed_set

    return precision, recall


def get_coverage(words, syntax_tree, tags, nodes):
    all_indices = set([key for key in tags.keys() if key is not None])
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

    return normalize(new_dict)

def normalize(dist):
    s = sum(dist.values())
    new_dist = {}
    for key, prob in dist.iteritems():
        new_dist[key] = prob/s
    return new_dist


def get_node_sequence(words, syntax_tree, tags, nodes):
    sequence = []







if __name__ == "__main__":
    tag_model, unary_model, binary_model = get_models()
    test_models(tag_model, unary_model, binary_model)