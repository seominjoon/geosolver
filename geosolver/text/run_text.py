import numpy as np
import networkx as nx
from geosolver.database.geoserver_interface import geoserver_interface
from geosolver.text.annotation_to_node import annotation_to_node, is_valid_annotation
from geosolver.text.decoder import TopDownLiftedDecoder
from geosolver.text.dependency_parser import stanford_parser
from geosolver.text.feature_function import UFF1
from geosolver.text.feature_function import BFF1
from geosolver.text.semantic_model import UnarySemanticModel
from geosolver.text.semantic_model import BinarySemanticModel
from geosolver.text.tag_model import CountBasedTagModel
from geosolver.text.transitions import string_to_words, node_to_semantic_rules, tag_rules_to_tags
from geosolver.text.transitions import node_to_tag_rules
from geosolver.utils import display_graph

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
    unary_model = UnarySemanticModel(UFF1)
    unary_model.fit(unary_rules, 1)
    binary_model = BinarySemanticModel(BFF1)
    binary_model.fit(binary_rules, 1)

    print unary_model.weights
    print binary_model.weights

    return tag_model, unary_model, binary_model



def test_models(tag_model, unary_model, binary_model):
    query = "annotated"
    questions = geoserver_interface.download_questions([query])
    semantics = geoserver_interface.download_semantics([query])
    for pk, question in questions.iteritems():
        for sentence_index, words in question.words.iteritems():
            words = replace(words)
            syntax_tree = stanford_parser.get_best_syntax_tree(words)
            tags = tag_model.get_best_tags(words, syntax_tree)
            decoder = TopDownLiftedDecoder(unary_model, binary_model)
            dist = decoder.get_formula_distribution(words, syntax_tree, tags)
            items = sorted(dist.items(), key=lambda x: x[1])
            print "---------------"
            print " ".join(words.values())
            for node, logp in items:
                # print(node_to_semantic_rules(words, syntax_tree, tags, node, True))
                print node, np.exp(logp)

if __name__ == "__main__":
    tag_model, unary_model, binary_model = get_models()
    test_models(tag_model, unary_model, binary_model)