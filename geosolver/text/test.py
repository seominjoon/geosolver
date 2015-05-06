import numpy as np
import networkx as nx
from geosolver.text.annotation_to_node import annotation_to_node
from geosolver.text.decoder import TopDownLiftedDecoder
from geosolver.text.feature_functions import UNARY_FEATURE_DIMENSION, bff1
from geosolver.text.feature_functions import BINARY_FEATURE_DIMENSION
from geosolver.text.feature_functions import uff1
from geosolver.text.semantic_model import UnarySemanticModel
from geosolver.text.semantic_model import BinarySemanticModel
from geosolver.text.tag_model import CountBasedTagModel
from geosolver.text.transitions import string_to_words, node_to_semantic_rules
from geosolver.text.transitions import node_to_tag_rules

__author__ = 'minjoon'

def get_models():
    sentence = "circle O has a radius of 5"
    words = string_to_words(sentence)
    syntax_tree = nx.DiGraph()
    annotation = "Equal@i(RadiusOf@4(Circle@0('O'@1)), [5]@6)"
    node = annotation_to_node(annotation)
    print(node)
    tag_rules = node_to_tag_rules(words, syntax_tree, node)
    print(tag_rules)
    tag_model = CountBasedTagModel(tag_rules)
    tags = tag_model.get_best_tags(words, syntax_tree)

    unary_rules, binary_rules = node_to_semantic_rules(words, syntax_tree, tags, node, lift_index=True)
    unary_initial_weights = np.zeros(UNARY_FEATURE_DIMENSION)
    binary_initial_weights = np.zeros(BINARY_FEATURE_DIMENSION)
    unary_model = UnarySemanticModel(uff1, unary_initial_weights)
    binary_model = BinarySemanticModel(bff1, binary_initial_weights)
    unary_model.optimize_weights(unary_rules, 0)
    binary_model.optimize_weights(binary_rules, 0)

    return tag_model, unary_model, binary_model




def test_models(tag_model, unary_model, binary_model):
    sentence = "O circle radius 5"
    words = string_to_words(sentence)
    syntax_tree = nx.DiGraph()
    tags = tag_model.get_best_tags(words, syntax_tree)
    decoder = TopDownLiftedDecoder(unary_model, binary_model)
    dist = decoder.get_formula_distribution(words, syntax_tree, tags)
    items = sorted(dist.items(), key=lambda x: x[1])
    for node, logp in items:
        # print(node_to_semantic_rules(words, syntax_tree, tags, node, True))
        print node, np.exp(logp)

if __name__ == "__main__":
    tag_model, unary_model, binary_model = get_models()
    test_models(tag_model, unary_model, binary_model)