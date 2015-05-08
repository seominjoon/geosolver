import itertools
from geosolver.text.dist_utils import is_log_consistent, log_normalize
from geosolver.text.dist_utils import log_add
from geosolver.text.ontology import function_signatures
from geosolver.text.semantic_model import UnarySemanticModel
from geosolver.text.semantic_model import BinarySemanticModel
from geosolver.text.rule import UnaryRule, BinaryRule
from geosolver.text.node import Node
from geosolver.text.transitions import node_to_semantic_rules

__author__ = 'minjoon'

class Decoder(object):
    def __init__(self, unary_semantic_model, binary_semantic_model):
        assert isinstance(unary_semantic_model, UnarySemanticModel)
        assert isinstance(binary_semantic_model, BinarySemanticModel)
        self.unary_semantic_model = unary_semantic_model
        self.binary_semantic_model = binary_semantic_model

    def get_formula_distribution(self, words, syntax_tree, tags, start="StartTruth"):
        return {}


class TopDownNaiveDecoder(Decoder):
    def get_formula_distribution(self, words, syntax_tree, tags, start="StartTruth"):
        """
        Returns a fully-grounded node : probability pair
        In naive case, this will be well-defined.

        :param words:
        :param syntax_tree:
        :param tags:
        :return:
        """
        def _recurse_unary(unary_rule, top_logp, excluding_indices):
            assert isinstance(unary_rule, UnaryRule)
            assert isinstance(excluding_indices, set)
            excluding_indices = excluding_indices.union({unary_rule.parent_index})


            if unary_rule.child_signature.is_leaf():
                child_nodes = {Node(unary_rule.child_index, unary_rule.child_signature, []): 0}
            elif unary_rule.child_signature.is_unary():
                distribution = self.unary_semantic_model.get_log_distribution(words, syntax_tree, tags,
                                                                              unary_rule.child_index, unary_rule.child_signature, excluding_indices)
                child_nodes = {}
                for current_unary_rule, logp in distribution.iteritems():
                    for node, logq in _recurse_unary(current_unary_rule, logp, excluding_indices).iteritems():
                        log_add(child_nodes, node, logq)
            elif unary_rule.child_signature.is_binary():
                distribution = self.binary_semantic_model.get_log_distribution(words, syntax_tree, tags,
                                                                               unary_rule.child_index, unary_rule.child_signature, excluding_indices)
                child_nodes = {}
                for current_binary_rule, logp in distribution.iteritems():
                    for node, logq in _recurse_binary(current_binary_rule, logp, excluding_indices).iteritems():
                        log_add(child_nodes, node, logq)

            if len(child_nodes) == 0:
                return {}

            parent_nodes = {Node(unary_rule.parent_index, unary_rule.parent_signature, [child_node]): top_logp + logp
                            for child_node, logp in child_nodes.iteritems()}
            return parent_nodes

        def _recurse_binary(binary_rule, top_logp, excluding_indices):
            assert isinstance(binary_rule, BinaryRule)
            assert isinstance(excluding_indices, set)
            excluding_indices = excluding_indices.union({binary_rule.parent_index})

            if binary_rule.a_signature.is_leaf():
                a_nodes = {Node(binary_rule.a_index, binary_rule.a_signature, []): 0}
            elif binary_rule.a_signature.is_unary():
                distribution = self.unary_semantic_model.get_log_distribution(words, syntax_tree, tags,
                                                                              binary_rule.a_index, binary_rule.a_signature, excluding_indices)
                a_nodes = {}
                for current_unary_rule, logp in distribution.iteritems():
                    for node, logq in _recurse_unary(current_unary_rule, logp, excluding_indices).iteritems():
                        log_add(a_nodes, node, logq)
            elif binary_rule.a_signature.is_binary():
                distribution = self.binary_semantic_model.get_log_distribution(words, syntax_tree, tags,
                                                                               binary_rule.a_index, binary_rule.a_signature, excluding_indices)
                a_nodes = {}
                for current_binary_rule, logp in distribution.iteritems():
                    for node, logq in _recurse_binary(current_binary_rule, logp, excluding_indices).iteritems():
                        log_add(a_nodes, node, logq)

            if binary_rule.b_signature.is_leaf():
                b_nodes = {Node(binary_rule.b_index, binary_rule.b_signature, []): 0}
            elif binary_rule.b_signature.is_unary():
                distribution = self.unary_semantic_model.get_log_distribution(words, syntax_tree, tags,
                                                                              binary_rule.b_index, binary_rule.b_signature, excluding_indices)
                b_nodes = {}
                for current_unary_rule, logp in distribution.iteritems():
                    for node, logq in _recurse_unary(current_unary_rule, logp, excluding_indices).iteritems():
                        log_add(b_nodes, node, logq)
            elif binary_rule.b_signature.is_binary():
                distribution = self.binary_semantic_model.get_log_distribution(words, syntax_tree, tags,
                                                                               binary_rule.b_index, binary_rule.b_signature, excluding_indices)
                b_nodes = {}
                for current_binary_rule, logp in distribution.iteritems():
                    for node, logq in _recurse_binary(current_binary_rule, logp, excluding_indices).iteritems():
                        log_add(b_nodes, node, logq)

            if len(a_nodes) == 0 or len(b_nodes) == 0:
                return {}

            parent_nodes = {}
            for a_node, b_node in itertools.product(a_nodes, b_nodes):
                node = Node(binary_rule.parent_index, binary_rule.parent_signature, [a_node, b_node])
                log_add(parent_nodes, node, top_logp + a_nodes[a_node] + b_nodes[b_node])

            return parent_nodes

        top_dist = self.unary_semantic_model.get_log_distribution(words, syntax_tree, tags,
                                                                  None, function_signatures[start])

        nodes = {}
        for start_unary_rule, logp in top_dist.iteritems():
            for node, logq in _recurse_unary(start_unary_rule, logp, set([])).iteritems():
                nodes[node] = logq

        return nodes

class TopDownLiftedDecoder(TopDownNaiveDecoder):
    def get_formula_distribution(self, words, syntax_tree, tags, start="StartTruth"):
        distribution = super(TopDownLiftedDecoder, self).get_formula_distribution(words, syntax_tree, tags, start=start)
        new_distribution = {}
        for node in distribution.keys():
            unary_rules, binary_rules = node_to_semantic_rules(words, syntax_tree, tags, node, True)
            unary_sum = sum(self.unary_semantic_model.get_log_prob(unary_rule) for unary_rule in unary_rules)
            binary_sum = sum(self.binary_semantic_model.get_log_prob(binary_rule) for binary_rule in binary_rules)
            new_distribution[node] = unary_sum + binary_sum

        normalized_distribution = log_normalize(new_distribution)
        return normalized_distribution

