import itertools
from scipy.optimize import minimize
import numpy as np
from geosolver.text.dist_utils import log_normalize
from geosolver.text.feature_function import FeatureFunction
from geosolver.text.ontology import function_signatures, issubtype
from geosolver.text.ontology_states import FunctionSignature
from geosolver.text.rule import SemanticRule, BinaryRule, UnaryRule

__author__ = 'minjoon'
class SemanticModel(object):
    def __init__(self, feature_function, initial_weights=None, initial_impliable_signatures=set(), localities = {}):
        assert isinstance(feature_function(), FeatureFunction)
        self.feature_function = feature_function
        if initial_weights is None:
            initial_weights = np.zeros(feature_function.dim)
        self.weights = initial_weights
        self.impliable_signatures = initial_impliable_signatures
        self.localities = localities
        self.feature_vectors = {}

    def fit(self, rules, reg_const):
        self._add_impliable_signatures(rules)
        self._optimize_weights(rules, reg_const)

    def _add_impliable_signatures(self, rules):
        for rule in rules:
            if isinstance(rule, UnaryRule):
                if rule.parent_index is None:
                    self.impliable_signatures.add(rule.parent_signature)
                if rule.child_index is None:
                    self.impliable_signatures.add(rule.child_signature)
            elif isinstance(rule, BinaryRule):
                if rule.parent_index is None:
                    self.impliable_signatures.add(rule.parent_signature)
                if rule.a_index is None:
                    self.impliable_signatures.add(rule.a_signature)
                if rule.b_index is None:
                    self.impliable_signatures.add(rule.b_signature)

    def _optimize_weights(self, rules, reg_const):
        """
        Obtain weights that maximizes the likelihood of the unary rules
        Log linear model with L2 regularization (ridge)
        Use L-BFGS-B for gradient descent
        Update the self.weights

        :param rules:
        :param reg_const:
        :return:
        """
        def loss_function(weights):
            model = self.__class__(self.feature_function, weights, self.impliable_signatures)
            return sum(model.get_log_prob(rule) for rule in rules) - \
                   0.5*reg_const*np.dot(weights, weights)

        def grad_function(weights):
            model = self.__class__(self.feature_function, weights, self.impliable_signatures)
            return sum(model.get_log_grad(rule) for rule in rules) - reg_const*weights

        negated_loss = lambda weights: -loss_function(weights)
        negated_grad = lambda weights: -grad_function(weights)

        result = minimize(negated_loss, self.weights, method='L-BFGS-B', jac=negated_grad)
        self.weights = result.x

    def get_log_distribution(self, words, syntax_tree, tags, parent_index, parent_signature, excluding_indices=set(),
                             lifted_rule=None):
        """
        dictionary of unary_rule : log probability pair
        The distribution must be well defined, i.e. must sum up to 1.
        To be implemented by the inheriting class

        :param words:
        :param syntax:
        :param tags:
        :param parent_index:
        :param parent_signature:
        :return:
        """
        assert isinstance(parent_signature, FunctionSignature)
        distribution = {}
        local_rules = self.get_possible_rules(words, syntax_tree, tags, parent_index, parent_signature, excluding_indices)
        for rule in local_rules:
            if lifted_rule is not None:
                if isinstance(rule, UnaryRule):
                    if rule.parent_signature == lifted_rule.parent_signature and rule.parent_index == lifted_rule.parent_index and \
                                    rule.child_index is None and rule.child_signature == lifted_rule.child_signature:
                        rule = lifted_rule
                elif isinstance(rule, BinaryRule):
                    a_index = rule.a_index
                    b_index = rule.b_index
                    if rule.parent_signature == lifted_rule.parent_signature and rule.parent_index == lifted_rule.parent_index and \
                                    rule.a_index is None and rule.a_signature == lifted_rule.a_signature:
                        a_index = lifted_rule.a_index
                    if rule.parent_signature == lifted_rule.parent_signature and rule.parent_index == lifted_rule.parent_index and \
                                    rule.b_index is None and rule.b_signature == lifted_rule.b_signature:
                        b_index = lifted_rule.b_index
                    rule = BinaryRule(words, syntax_tree, tags, parent_index, parent_signature, a_index, rule.a_signature,
                                      b_index, rule.b_signature)
            if rule in self.feature_vectors:
                feature_vector = self.feature_vectors[rule]
            else:
                feature_vector = self.feature_function.evaluate(rule)
                self.feature_vectors[rule] = feature_vector
            numerator = np.dot(self.weights, feature_vector)
            distribution[rule] = numerator

        # print distribution
        if len(distribution) == 0:
            return distribution

        normalized_distribution = log_normalize(distribution)
        return normalized_distribution

    def get_log_prob(self, rule, excluding_indices=set(), lifted=False):
        assert isinstance(rule, SemanticRule)
        distribution = self.get_log_distribution(rule.words, rule.syntax_tree, rule.tags, rule.parent_index,
                                                 rule.parent_signature, excluding_indices,
                                                 lifted_rule=rule)
        if rule in distribution:
            return distribution[rule]
        else:
            print(rule)
            print(rule.words)
            print(rule.tags)
            print(distribution)
            raise Exception()

        return -np.inf

    def get_log_grad(self, rule, excluding_indices=set()):
        distribution = self.get_log_distribution(rule.words, rule.syntax_tree, rule.tags, rule.parent_index,
                                                 rule.parent_signature, excluding_indices)
        log_grad = self.feature_function.evaluate(rule) - sum(np.exp(logp) * self.feature_function.evaluate(each_rule)
                                                     for each_rule, logp in distribution.iteritems())
        return log_grad

    def get_possible_rules(self, words, syntax_tree, tags, parent_index, parent_signature, excluding_indices=set()):
        """
        NEED TO BE OVERRIDDEN
        Need to enforce type-matching here! That is, get only rules consistent with the ontology.
        (perhaps remove equivalent rules. For instance, equality. but this might be bad.. or add symmetry feature)

        :param words:
        :param syntax_tree:
        :param tags:
        :param parent_index:
        :param parent_signature:
        :param excluding_indices:
        :return list:
        """
        assert False
        return []

class UnarySemanticModel(SemanticModel):
    def get_possible_rules(self, words, syntax_tree, tags, parent_index, parent_signature, excluding_indices=set()):
        assert isinstance(parent_signature, FunctionSignature)
        assert parent_signature.is_unary()
        excluding_indices = set(excluding_indices)
        if parent_index is not None:
            excluding_indices.add(parent_index)

        all_indices = set(words.keys())
        if parent_index is not None and tags[parent_index] in self.localities:
            locality = self.localities[tags[parent_index]]
            all_indices = all_indices.intersection(set(range(parent_index-locality, parent_index+locality+1)))
        available_indices = all_indices.difference(excluding_indices).union(function_signatures.values())
        rules = []

        for child_index in available_indices:
            if isinstance(child_index, int):
                child_signature = tags[child_index]
                if child_signature is None:
                    continue
            elif isinstance(child_index, FunctionSignature):
                child_signature = child_index
                child_index = None
                if child_signature not in self.impliable_signatures:
                    continue
            else:
                raise Exception()

            if issubtype(child_signature.return_type, parent_signature.arg_types[0]):
                # ontology enforcement
                rule = UnaryRule(words, syntax_tree, tags, parent_index, parent_signature, child_index, child_signature)
                rules.append(rule)

        # assert len(rules) > 0
        return rules


class BinarySemanticModel(SemanticModel):
    def get_possible_rules(self, words, syntax_tree, tags, parent_index, parent_signature, excluding_indices=set()):
        assert isinstance(parent_signature, FunctionSignature)
        assert parent_signature.is_binary()
        excluding_indices = set(excluding_indices)
        if parent_index is not None:
            excluding_indices.add(parent_index)
        all_indices = set(words.keys())
        if parent_index is not None and tags[parent_index] in self.localities:
            locality = self.localities[tags[parent_index]]
            all_indices = all_indices.intersection(set(range(parent_index-locality, parent_index+locality+1)))
        available_indices = set(all_indices).difference(excluding_indices).union(function_signatures.values())
        rules = []

        for a_index, b_index in itertools.product(available_indices, repeat=2):
            # i.e. argument order matters, but no duplicate except implications
            if a_index == b_index and isinstance(a_index, int):
                continue

            if isinstance(a_index, int):
                a_signature = tags[a_index]
                if a_signature is None:
                    continue
            elif isinstance(a_index, FunctionSignature):
                a_signature = a_index
                a_index = None
                if a_signature not in self.impliable_signatures:
                    continue

            if isinstance(b_index, int):
                b_signature = tags[b_index]
                if b_signature is None:
                    continue
            elif isinstance(b_index, FunctionSignature):
                b_signature = b_index
                b_index = None
                if b_signature not in self.impliable_signatures:
                    continue

            if issubtype(a_signature.return_type, parent_signature.arg_types[0]) and \
                    issubtype(b_signature.return_type, parent_signature.arg_types[1]):
                # ontology enforcement
                rule = BinaryRule(words, syntax_tree, tags, parent_index, parent_signature,
                                  a_index, a_signature, b_index, b_signature)
                rules.append(rule)

        assert len(rules) > 0
        return rules

