import itertools
from scipy.optimize import minimize
import numpy as np
from geosolver.text.dist_utils import log_normalize
from geosolver.text.ontology import function_signatures
from geosolver.text.ontology_states import FunctionSignature
from geosolver.text.rule import SemanticRule, BinaryRule, UnaryRule

__author__ = 'minjoon'
class SemanticModel(object):
    def __init__(self, feature_function, initial_weights):
        self.feature_function = feature_function
        self.weights = initial_weights

    def optimize_weights(self, rules, reg_const):
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
            model = self.__class__(self.feature_function, weights)
            return sum(model.get_log_prob(rule) for rule in rules) - \
                   0.5*reg_const*np.dot(weights, weights)

        def grad_function(weights):
            model = self.__class__(self.feature_function, weights)
            return sum(model.get_log_grad(rule) for rule in rules) - reg_const*weights

        negated_loss = lambda weights: -loss_function(weights)
        negated_grad = lambda weights: -grad_function(weights)

        result = minimize(negated_loss, self.weights, method='L-BFGS-B', jac=negated_grad)
        self.weights = result.x

    def get_log_distribution(self, words, syntax_tree, tags, parent_index, parent_signature, excluding_indices=(),
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

            features = self.feature_function(rule)
            numerator = np.dot(self.weights, features)
            distribution[rule] = numerator

        normalized_distribution = log_normalize(distribution)

        return normalized_distribution

    def get_log_prob(self, rule, excluding_indices=(), lifted=False):
        assert isinstance(rule, SemanticRule)
        distribution = self.get_log_distribution(rule.words, rule.syntax_tree, rule.tags, rule.parent_index,
                                                 rule.parent_signature, excluding_indices,
                                                 lifted_rule=rule)
        if rule in distribution:
            return distribution[rule]
        else:
            print(rule)
            print(distribution)

        return -np.inf

    def get_log_grad(self, rule, excluding_indices=()):
        distribution = self.get_log_distribution(rule.words, rule.syntax_tree, rule.tags, rule.parent_index,
                                                 rule.parent_signature, excluding_indices)
        log_grad = self.feature_function(rule) - sum(np.exp(logp) * self.feature_function(each_rule)
                                                     for each_rule, logp in distribution.iteritems())
        return log_grad

    def get_possible_rules(self, words, syntax_tree, tags, parent_index, parent_signature, excluding_indices=()):
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
    def get_possible_rules(self, words, syntax_tree, tags, parent_index, parent_signature, excluding_indices=()):
        assert isinstance(parent_signature, FunctionSignature)
        assert parent_signature.is_unary()
        excluding_indices = set(excluding_indices)
        excluding_indices.add(parent_index)
        available_indices = set(words.keys()).difference(excluding_indices).union(function_signatures.values())
        rules = []
        for child_index in available_indices:
            if isinstance(child_index, int):
                child_signature = tags[child_index]
            else:
                assert isinstance(child_index, FunctionSignature)
                child_signature = child_index
                child_index = None

            if parent_signature is None or child_signature is None:
                continue

            if parent_signature.arg_types[0] == child_signature.return_type:
                # ontology enforcement
                rule = UnaryRule(words, syntax_tree, tags, parent_index, parent_signature, child_index, child_signature)
                rules.append(rule)
        return rules


class BinarySemanticModel(SemanticModel):
    def get_possible_rules(self, words, syntax_tree, tags, parent_index, parent_signature, excluding_indices=()):
        assert isinstance(parent_signature, FunctionSignature)
        assert parent_signature.is_binary()
        excluding_indices = set(excluding_indices)
        excluding_indices.add(parent_index)
        available_indices = set(words.keys()).difference(excluding_indices).union(function_signatures.values())
        rules = []
        for a_index, b_index in itertools.permutations(available_indices, 2):
            # i.e. argument order matters, but no duplicate (this might not be true in future)
            if isinstance(a_index, int):
                a_signature = tags[a_index]
            else:
                a_signature = a_index
                a_index = None
            if isinstance(b_index, int):
                b_signature = tags[b_index]
            else:
                b_signature = b_index
                b_index = None

            if parent_signature is None or a_signature is None or b_signature is None:
                continue

            if tuple(parent_signature.arg_types) == (a_signature.return_type, b_signature.return_type):
                # ontology enforcement
                rule = BinaryRule(words, syntax_tree, tags, parent_index, parent_signature,
                                  a_index, a_signature, b_index, b_signature)
                rules.append(rule)
        return rules

