import itertools
import numpy as np
import scipy

__author__ = 'minjoon'


class FunctionSignature(object):
    def __init__(self, name, return_type, arg_types):
        self.name = name
        self.return_type = return_type
        self.arg_types = arg_types

    def is_leaf(self):
        return len(self.arg_types) == 0

    def is_unary(self):
        return len(self.arg_types) == 1

    def is_binary(self):
        return len(self.arg_types) == 2


    def __hash__(self):
        return hash((self.name, self.return_type, tuple(self.arg_types)))


def add_function_signature(signatures, signature_tuple):
    name, return_type, arg_types = signature_tuple
    assert name not in signatures
    signatures[name] = FunctionSignature(name, return_type, arg_types)


types = ['start', 'number', 'modifier', 'circle', 'line', 'truth']
function_signatures = {}
tuples = (
    ('StartTruth', 'start', ['truth']),
    ('RadiusOf', 'number', ['circle']),
    ('Equal', 'truth', ['number', 'number']),
    ('Circle', 'circle', ['modifier']),
)
for tuple_ in tuples:
    add_function_signature(function_signatures, tuple_)


class Node(object):
    def __init__(self, function_signature, children):
        assert isinstance(function_signature, FunctionSignature)
        for child in children:
            assert isinstance(child, Node)

        self.function_signature = function_signature
        self.children = children

    def __hash__(self):
        return hash((self.function_signature, tuple(self.children)))


class TagRule(object):
    def __init__(self, words, syntax_tree, index, signature):
        self.words = words
        self.syntax_tree = syntax_tree
        self.index = index
        self.signature = signature


class DeterministicTagModel(object):
    def __init__(self, tag_rules, feature_function):
        pass

    def get_tag_distribution(self, words, syntax_tree, index):
        """
        Returns a dictionary of signature:probability pair
        :param words:
        :param syntax_tree:
        :param index:
        :return:
        """

    def get_best_tag(self, words, syntax_tree, index):
        if words[index] == 'radius':
            return function_signatures['RadiusOf'], 0.0
        elif words[index] == 'circle':
            return function_signatures['Circle'], 0.0
        elif words[index] == 'O':
            return FunctionSignature('O', 'modifier', []), 0.0
        elif words[index] == '5':
            return FunctionSignature('5', 'number', []), 0.0
        else:
            return None, 0.0


class UnaryRule(object):
    def __init__(self, words, syntax_tree, tags, parent_index, parent_signature, child_index, child_signature):
        self.words = words
        self.syntax_tree = syntax_tree
        self.tags = tags
        self.parent_index = parent_index
        self.parent_signature = parent_signature
        self.child_index = child_index
        self.child_signature = child_signature

    def __hash__(self):
        return hash((self.parent_index, self.parent_signature, self.child_index, self.child_signature))


class BinaryRule(object):
    def __init__(self, words, syntax_tree, tags,
                 parent_index, parent_signature, a_index, a_signature, b_index, b_signature):
        self.words = words
        self.syntax_tree = syntax_tree
        self.tags = tags
        self.parent_index = parent_index
        self.parent_signature = parent_signature
        self.a_index = a_index
        self.a_signature = a_signature
        self.b_index = b_index
        self.b_signature = b_signature

    def __hash__(self):
        return hash((self.parent_index, self.parent_signature,
                     self.a_index, self.a_signature, self.b_index, self.b_signature))


def uff1(unary_rule):
    # TODO : implement feature function
    assert False
    return np.array([])

def bff1(binary_rule):
    """
    binary feature function version 1
    Usually, this will depend on unary feature function.

    :param binary_rule:
    :return:
    """
    # TODO : implement feature function
    assert False
    return np.array([])

class SemanticModel(object):
    def __init__(self, feature_function, initial_weights):
        self.feature_function = feature_function
        self.weights = initial_weights

    def optimize_weights(self, rules, reg_const):
        """
        Obtain weights that maximizes the likelihood of the unary rules
        Log linear model with L2 regularization (ridge)
        Use BFGS for gradient descent
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

        optimized_weights = scipy.optimize.minimize(negated_loss, self.weights, method='BFGS', jac=negated_grad)
        self.weights = optimized_weights

    def get_log_distribution(self, words, syntax_tree, tags, parent_index, parent_signature, excluding_indices=()):
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
        distribution = {}
        local_unary_rules = self.get_possible_rules(words, syntax_tree, tags, parent_index, parent_signature,
                                                    excluding_indices)
        for unary_rule in local_unary_rules:
            features = self.feature_function(unary_rule)
            numerator = np.dot(self.weights, features)
            distribution[unary_rule] = numerator

        normalized_distribution = log_normalize(distribution)

        return normalized_distribution

    def get_log_prob(self, rule, excluding_indices=()):
        assert isinstance(rule, UnaryRule)
        distribution = self.get_log_distribution(rule.words, rule.tags, rule.parent_index,
                                                 rule.parent_signature, excluding_indices)
        if rule in distribution:
            return distribution[rule]

        return -np.inf

    def get_log_grad(self, rule, excluding_indices=()):
        distribution = self.get_log_distribution(rule.words, rule.tags, rule.parent_index,
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


def log_normalize(distribution):
    sum_value = sum(logp for _, logp in distribution)
    normalized_distribution = {key: value-sum_value for key, value in distribution.iteritems()}
    return normalized_distribution


class UnarySemanticModel(SemanticModel):
    def get_possible_rules(self, words, syntax_tree, tags, parent_index, parent_signature, excluding_indices=()):
        assert False
        return []


class BinarySemanticModel(SemanticModel):
    def get_possible_rules(self, words, syntax_tree, tags, parent_index, parent_signature, excluding_indices=()):
        assert False
        return []


class TopDownNaiveDecoder(object):
    def __init__(self, unary_semantic_model, binary_semantic_model):
        assert isinstance(unary_semantic_model, UnarySemanticModel)
        assert isinstance(binary_semantic_model, BinarySemanticModel)
        self.unary_semantic_model = unary_semantic_model
        self.binary_semantic_model = binary_semantic_model

    def get_formula_distribution(self, words, syntax_tree, tags):
        """
        Returns a fully-grounded node : probability pair
        In naive case, this will be well-defined.

        :param words:
        :param syntax_tree:
        :param tags:
        :return:
        """

        # TODO : enforce non-redundancy within formula
        # TODO : since this is top-down, no syntactic feature for implied functions. Reweight formulas in another method

        def _recurse_unary(unary_rule, excluding_indices):
            assert isinstance(unary_rule, UnaryRule)
            assert isinstance(excluding_indices, set)
            excluding_indices = excluding_indices.union({unary_rule.parent_index})

            if unary_rule.child_signature.is_leaf():
                child_nodes = {Node(unary_rule.child_signature, []): 0}
            elif unary_rule.child_signature.is_unary():
                distribution = self.unary_semantic_model.get_log_distribution(words, syntax_tree, tags,
                    unary_rule.child_index, unary_rule.child_signature, excluding_indices)
                child_nodes = {node: logp + logq
                               for current_unary_rule, logp in distribution.iteritems()
                               for node, logq in _recurse_unary(current_unary_rule).iteritems()}
            elif unary_rule.child_signature.is_binary():
                distribution = self.binary_semantic_model.get_log_distribution(words, syntax_tree, tags,
                    unary_rule.child_index, unary_rule.child_signature, excluding_indices)
                child_nodes = {node: logp + logq
                               for current_binary_rule, logp in distribution.iteritems()
                               for node, logq in _recurse_binary(current_binary_rule).iteritems()}

            parent_nodes = [Node(unary_rule.parent_signature, [child_node]) for child_node in child_nodes]
            return parent_nodes

        def _recurse_binary(binary_rule, excluding_indices):
            assert isinstance(binary_rule, BinaryRule)
            assert isinstance(excluding_indices, set)
            excluding_indices = excluding_indices.union({binary_rule.parent_index})

            if binary_rule.a_signature.is_leaf():
                a_nodes = {Node(binary_rule.a_signature, []): 0}
            elif binary_rule.a_signature.is_unary():
                distribution = self.unary_semantic_model.get_log_distribution(words, syntax_tree, tags,
                        binary_rule.a_index, binary_rule.a_signature, excluding_indices)
                a_nodes = {node: logp + logq
                           for current_unary_rule, logp in distribution.iteritems()
                           for node, logq in _recurse_unary(current_unary_rule).iteritems()}
            elif binary_rule.a_signature.is_binary():
                distribution = self.binary_semantic_model.get_log_distribution(words, syntax_tree, tags,
                        binary_rule.a_index, binary_rule.a_signature, excluding_indices)
                a_nodes = {node: logp + logq
                           for current_binary_rule, logp in distribution.iteritems()
                           for node, logq in _recurse_binary(current_binary_rule).iteritems()}

            if binary_rule.b_signature.is_leaf():
                b_nodes = {Node(binary_rule.b_signature, []): 0}
            elif binary_rule.b_signature.is_unary():
                distribution = self.unary_semantic_model.get_log_distribution(words, syntax_tree, tags,
                    binary_rule.b_index, binary_rule.b_signature, excluding_indices)
                b_nodes = {node: logp + logq
                           for current_unary_rule, logp in distribution.iteritems()
                           for node, logq in _recurse_unary(current_unary_rule).iteritems()}
            elif binary_rule.b_signature.is_binary():
                distribution = self.binary_semantic_model.get_log_distribution(words, syntax_tree, tags,
                    binary_rule.b_index, binary_rule.b_signature, excluding_indices)
                b_nodes = {node: logp + logq
                           for current_binary_rule, logp in distribution.iteritems()
                           for node, logq in _recurse_binary(current_binary_rule).iteritems()}

            parent_nodes = {Node(binary_rule.parent_signature, [a_node, b_node]): a_nodes[a_node] + b_nodes[b_node]
                            for a_node, b_node in itertools.product(a_nodes, b_nodes)}

            return parent_nodes

        start_unary_rules = self.unary_semantic_model.get_possible_rules(words, syntax_tree, tags, None,
                                                                         function_signatures['StartTruth'])
        nodes = dict(itertools.chain(*(_recurse_unary(start_unary_rule).iteritems()
                                       for start_unary_rule in start_unary_rules)))

        return nodes

