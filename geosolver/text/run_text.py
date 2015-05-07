import numpy as np
import networkx as nx
from geosolver.text.annotation_to_node import annotation_to_node
from geosolver.text.decoder import TopDownLiftedDecoder
from geosolver.text.dependency_parser import stanford_parser
from geosolver.text.feature_functions import UFF1
from geosolver.text.feature_functions import BFF1
from geosolver.text.semantic_model import UnarySemanticModel
from geosolver.text.semantic_model import BinarySemanticModel
from geosolver.text.tag_model import CountBasedTagModel
from geosolver.text.transitions import string_to_words, node_to_semantic_rules
from geosolver.text.transitions import node_to_tag_rules
from geosolver.utils import display_graph

__author__ = 'minjoon'

def get_models():
    sentence = "circle O has a radius of 5"
    words = string_to_words(sentence)
    syntax_tree = stanford_parser.get_best_syntax_tree(words)
    syntax_tree = syntax_tree.to_undirected()
    annotation = "Equal@i(RadiusOf@4(Circle@0('O'@1)), [5]@6)"
    node = annotation_to_node(annotation)
    tag_rules = node_to_tag_rules(words, syntax_tree, node)
    tag_model = CountBasedTagModel(tag_rules)
    tags = tag_model.get_best_tags(words, syntax_tree)

    unary_rules, binary_rules = node_to_semantic_rules(words, syntax_tree, tags, node, lift_index=True)
    unary_model = UnarySemanticModel(UFF1)
    binary_model = BinarySemanticModel(BFF1)
    unary_model.fit(unary_rules, 0)
    binary_model.fit(binary_rules, 0)
    print unary_rules, unary_model.weights
    print binary_model.weights

    return tag_model, unary_model, binary_model




def test_models(tag_model, unary_model, binary_model):
    sentence = "circle O has a radius of 5 and the circle B is smaller."
    words = string_to_words(sentence)
    syntax_tree = stanford_parser.get_best_syntax_tree(words)
    syntax_tree = syntax_tree.to_undirected()
    # display_graph(syntax_tree)
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