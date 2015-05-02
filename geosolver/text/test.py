import itertools
import numpy as np
from scipy.optimize import minimize
import networkx as nx

__author__ = 'minjoon'


class FunctionSignature(object):
    def __init__(self, name, return_type, arg_types, is_symmetric=False):
        self.name = name
        self.return_type = return_type
        self.arg_types = arg_types
        self.is_symmetric = is_symmetric

    def is_leaf(self):
        return len(self.arg_types) == 0

    def is_unary(self):
        return len(self.arg_types) == 1

    def is_binary(self):
        return len(self.arg_types) == 2

    def __hash__(self):
        return hash((self.name, self.return_type, tuple(self.arg_types)))

    def __repr__(self):
        return "%s %s(%s)" % (self.return_type, self.name, ", ".join(self.arg_types))

    def __eq__(self, other):
        return repr(self) == repr(other)


def add_function_signature(signatures, signature_tuple):
    if len(signature_tuple) == 3:
        name, return_type, arg_types = signature_tuple
        is_symmetric = False
    elif len(signature_tuple) == 4:
        name, return_type, arg_types, is_symmetric = signature_tuple
    assert name not in signatures
    signatures[name] = FunctionSignature(name, return_type, arg_types, is_symmetric)


types = ['root', 'start', 'number', 'modifier', 'circle', 'line', 'truth']
function_signatures = {}
tuples = (
    ('Root', 'root', ['start']),
    ('StartTruth', 'start', ['truth']),
    ('RadiusOf', 'number', ['circle']),
    ('Equal', 'truth', ['number', 'number'], True),
    ('Circle', 'circle', ['modifier']),
    ('The', 'modifier', []),
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
        if self.function_signature.is_symmetric:
            return hash((self.function_signature, frozenset(self.children)))
        return hash((self.function_signature, tuple(self.children)))

    def __eq__(self, other):
        if self.function_signature.is_symmetric:
            print set(self.children) == set(other.children), self.children, other.children
            return self.function_signature == other.function_signature and set(self.children) == set(other.children)
        return repr(self) == repr(other)

    def __repr__(self):
        if len(self.children) == 0:
            return "%s %s" % (self.function_signature.return_type, self.function_signature.name)

        args_string = ", ".join(repr(child) for child in self.children)
        return "%s(%s)" % (self.function_signature.name, args_string)


class TagRule(object):
    def __init__(self, words, syntax_tree, index, signature):
        self.words = words
        self.syntax_tree = syntax_tree
        self.index = index
        self.signature = signature

    def __repr__(self):
        return "%r->%s" % (self.index, self.signature.name)

    def __eq__(self, other):
        return repr(self) == repr(other)


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
        elif words[index] == 'the':
            return function_signatures['The'], np.log(0.1)
        else:
            return None, 0.0

    def get_best_tags(self, words, syntax_tree):
        tags = {index: self.get_best_tag(words, syntax_tree, index)[0] for index in words.keys()}
        return tags



class UnaryRule(object):
    def __init__(self, words, syntax_tree, tags, parent_index, parent_signature, child_index, child_signature):
        assert isinstance(parent_signature, FunctionSignature)
        assert isinstance(child_signature, FunctionSignature)
        assert isinstance(parent_index, int) or parent_index is None
        assert isinstance(child_index, int) or child_index is None
        self.words = words
        self.syntax_tree = syntax_tree
        self.tags = tags
        self.parent_index = parent_index
        self.parent_signature = parent_signature
        self.child_index = child_index
        self.child_signature = child_signature

    def __hash__(self):
        return hash((self.parent_index, self.parent_signature, self.child_index, self.child_signature))

    def __repr__(self):
        return "%s@%r->%s@%r" % (self.parent_signature.name, self.parent_index,
                                 self.child_signature.name, self.child_index)

    def __eq__(self, other):
        return repr(self) == repr(other)



class BinaryRule(object):
    def __init__(self, words, syntax_tree, tags,
                 parent_index, parent_signature, a_index, a_signature, b_index, b_signature):
        assert isinstance(parent_signature, FunctionSignature)
        assert isinstance(a_signature, FunctionSignature)
        assert isinstance(b_signature, FunctionSignature)
        assert isinstance(parent_index, int) or parent_index is None
        assert isinstance(a_index, int) or a_index is None
        assert isinstance(b_index, int) or b_index is None
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

    def __repr__(self):
        return "%s@%r->%s@%r|%s@%r" % (self.parent_signature.name, self.parent_index,
                                        self.a_signature.name, self.a_index,
                                        self.b_signature.name, self.b_index)

    def __eq__(self, other):
        return repr(self) == repr(other)


UNARY_FEATURE_DIMENSION = 4
BINARY_FEATURE_DIMENSION = 2*UNARY_FEATURE_DIMENSION + 3

def uff1(unary_rule):
    # For now, just distance between them in dependency tree and sentence and their product
    assert isinstance(unary_rule, UnaryRule)
    if unary_rule.parent_index is not None and unary_rule.child_index is not None:
        f2 = abs(unary_rule.parent_index - unary_rule.child_index)
        # f1 = nx.shortest_path_length(unary_rule.syntax_tree, unary_rule.parent_index, unary_rule.child_index)
        f1 = f2
    else:
        f1 = len(unary_rule.words)/2.0
        f2 = f1
    f3 = np.sqrt(f1*f2)
    f4 = int(unary_rule.child_signature.is_leaf())
    out = np.array([f1, f2, f3, f4])
    assert len(out) == UNARY_FEATURE_DIMENSION
    return out


def bff1(binary_rule):
    """
    binary feature function version 1
    Usually, this will depend on unary feature function.

    :param binary_rule:
    :return:
    """
    assert isinstance(binary_rule, BinaryRule)
    unary_rule_a = UnaryRule(binary_rule.words, binary_rule.syntax_tree, binary_rule.tags, binary_rule.parent_index,
                             binary_rule.parent_signature, binary_rule.a_index, binary_rule.a_signature)
    unary_rule_b = UnaryRule(binary_rule.words, binary_rule.syntax_tree, binary_rule.tags, binary_rule.parent_index,
                             binary_rule.parent_signature, binary_rule.b_index, binary_rule.b_signature)
    if binary_rule.a_index is not None and binary_rule.b_index is not None:
        f2 = abs(binary_rule.a_index - binary_rule.b_index)
        # f1 = nx.shortest_path_length(binary_rule.syntax_tree, binary_rule.a_index, binary_rule.b_index)
        f1 = f2**2
    else:
        f1 = len(binary_rule.words)/2.0
        f2 = f1**2
    f3 = np.sqrt(f1*f2)

    a1 = uff1(unary_rule_a)
    a2 = uff1(unary_rule_b)
    a3 = [f1, f2, f3]

    out = np.array(list(itertools.chain(a1, a2, a3)))
    assert len(out) == BINARY_FEATURE_DIMENSION
    return out


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

        result = minimize(negated_loss, self.weights, method='BFGS', jac=negated_grad)
        self.weights = result.x

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
        assert isinstance(parent_signature, FunctionSignature)
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
        assert isinstance(rule, UnaryRule) or isinstance(rule, BinaryRule)
        distribution = self.get_log_distribution(rule.words, rule.syntax_tree, rule.tags, rule.parent_index,
                                                 rule.parent_signature, excluding_indices)
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


def log_normalize(distribution):
    log_sum_value = np.log(sum(np.exp(logp) for _, logp in distribution.iteritems()))
    normalized_distribution = {key: value - log_sum_value for key, value in distribution.iteritems()}
    assert is_log_consistent(normalized_distribution)
    return normalized_distribution


def is_log_consistent(distribution, eps=0.01):
    sum_value = sum(np.exp(logp) for _, logp in distribution.iteritems())
    print(sum_value)
    return np.abs(1-sum_value) < eps


def log_add(distribution, key, logp):
    if key in distribution:
        distribution[key] = np.log(np.exp(distribution[key]) + np.exp(logp))
    else:
        distribution[key] = logp


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


class TopDownNaiveDecoder(object):
    def __init__(self, unary_semantic_model, binary_semantic_model):
        assert isinstance(unary_semantic_model, UnarySemanticModel)
        assert isinstance(binary_semantic_model, BinarySemanticModel)
        self.unary_semantic_model = unary_semantic_model
        self.binary_semantic_model = binary_semantic_model

    def get_formula_distribution(self, words, syntax_tree, tags, start="StartTruth"):
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

        def _recurse_unary(unary_rule, top_logp, excluding_indices):
            assert isinstance(unary_rule, UnaryRule)
            assert isinstance(excluding_indices, set)
            excluding_indices = excluding_indices.union({unary_rule.parent_index})

            if unary_rule.child_signature.is_leaf():
                child_nodes = {Node(unary_rule.child_signature, []): 0}
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

            print(unary_rule)
            for node, logp in child_nodes.iteritems():
                print node, np.exp(logp)
            assert is_log_consistent(child_nodes)

            parent_nodes = {Node(unary_rule.parent_signature, [child_node]): top_logp + logp
                            for child_node, logp in child_nodes.iteritems()}
            return parent_nodes

        def _recurse_binary(binary_rule, top_logp, excluding_indices):
            assert isinstance(binary_rule, BinaryRule)
            assert isinstance(excluding_indices, set)
            excluding_indices = excluding_indices.union({binary_rule.parent_index})

            if binary_rule.a_signature.is_leaf():
                a_nodes = {Node(binary_rule.a_signature, []): 0}
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
                    for node, logq in _recurse_binary(binary_rule, logp, excluding_indices).iteritems():
                        log_add(a_nodes, node, logq)

            if binary_rule.b_signature.is_leaf():
                b_nodes = {Node(binary_rule.b_signature, []): 0}
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
                    for node, logq in _recurse_binary(binary_rule, logp, excluding_indices).iteritems():
                        log_add(b_nodes, node, logq)

            assert is_log_consistent(a_nodes)
            assert is_log_consistent(b_nodes)

            parent_nodes = {Node(binary_rule.parent_signature, [a_node, b_node]):
                            top_logp + a_nodes[a_node] + b_nodes[b_node]
                            for a_node, b_node in itertools.product(a_nodes, b_nodes)}

            return parent_nodes

        top_dist = self.unary_semantic_model.get_log_distribution(words, syntax_tree, tags,
                                                                      None, function_signatures[start])

        """
        nodes = dict(itertools.chain(*[_recurse_unary(start_unary_rule, 1.0, set([])).iteritems()
                                       for start_unary_rule in start_unary_rules]))
        """

        nodes = {}
        for start_unary_rule, logp in top_dist.iteritems():
            for node, logq in _recurse_unary(start_unary_rule, logp, set([])).iteritems():
                nodes[node.children[0]] = logq

        return nodes


def tuple_to_tag_rules(words, syntax_tree, tuple_):
    splitter = '@'
    implication = 'i'
    tag_rules = []
    for string in tuple_:
        function_name, index = string.split(splitter)
        if function_name in function_signatures:
            function_signature = function_signatures[function_name]
        elif (function_name[0], function_name[-1]) == tuple("''"):
            function_signature = FunctionSignature(function_name[1:-1], 'modifier', [])
        elif (function_name[0], function_name[-1]) == tuple("[]"):
            function_signature = FunctionSignature(function_name[1:-1], 'number', [])
        elif (function_name[0], function_name[-1]) == tuple("<>"):
            function_signature = FunctionSignature(function_name[1:-1], 'variable', [])
        else:
            raise Exception()

        if index == implication:
            index = None
        else:
            index = int(index)
        tag_rule = TagRule(words, syntax_tree, index, function_signature)
        tag_rules.append(tag_rule)
    return tag_rules


def tuples_to_semantic_rules(words, syntax_tree, tuples):
    tag_rules_list = [tuple_to_tag_rules(words, syntax_tree, tuple_) for tuple_ in tuples]
    tags = {tag_rule.index: tag_rule.signature for tag_rule in itertools.chain(*tag_rules_list)}
    for index in words:
        if index not in tags:
            tags[index] = None

    unary_rules = []
    binary_rules = []
    for tag_rules in tag_rules_list:
        if len(tag_rules) == 2:
            unary_rule = UnaryRule(words, syntax_tree, tags, tag_rules[0].index, tag_rules[0].signature,
                                   tag_rules[1].index, tag_rules[1].signature)
            unary_rules.append(unary_rule)
        elif len(tag_rules) == 3:
            binary_rule = BinaryRule(words, syntax_tree, tags, tag_rules[0].index, tag_rules[0].signature,
                                     tag_rules[1].index, tag_rules[1].signature,
                                     tag_rules[2].index, tag_rules[2].signature)
            binary_rules.append(binary_rule)
    return unary_rules, binary_rules

def string_to_words(string):
    word_list = string.split(' ')
    words = {index: word_list[index] for index in range(len(word_list))}
    return words

def get_models():
    sentence = "circle O has a radius of 5"
    words = string_to_words(sentence)
    syntax_tree = nx.DiGraph()
    tuples = (
        ('StartTruth@i', 'Equal@i'),
        ('Equal@i', 'RadiusOf@4', '[5]@6'),
        ('RadiusOf@4', 'Circle@0'),
        ('Circle@0', "'O'@1"),
    )
    tag_rules = list(itertools.chain(*[tuple_to_tag_rules(words, syntax_tree, tuple_) for tuple_ in tuples]))
    tagging_feature_function = lambda x: None

    unary_rules, binary_rules = tuples_to_semantic_rules(words, syntax_tree, tuples)
    tag_model = DeterministicTagModel(tag_rules, tagging_feature_function)
    unary_initial_weights = np.zeros(UNARY_FEATURE_DIMENSION)
    binary_initial_weights = np.zeros(BINARY_FEATURE_DIMENSION)
    unary_model = UnarySemanticModel(uff1, unary_initial_weights)
    binary_model = BinarySemanticModel(bff1, binary_initial_weights)
    unary_model.optimize_weights(unary_rules, 1)
    binary_model.optimize_weights(binary_rules, 1)

    return tag_model, unary_model, binary_model


def test_models(tag_model, unary_model, binary_model):
    sentence = "the radius circle O is 5"
    words = string_to_words(sentence)
    syntax_tree = nx.DiGraph()

    tags = tag_model.get_best_tags(words, syntax_tree)
    decoder = TopDownNaiveDecoder(unary_model, binary_model)
    dist = decoder.get_formula_distribution(words, syntax_tree, tags)
    items = sorted(dist.items(), key=lambda x: x[1])
    for node, logp in items:
        print node, np.exp(logp)

if __name__ == "__main__":
    tag_model, unary_model, binary_model = get_models()
    test_models(tag_model, unary_model, binary_model)