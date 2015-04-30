import itertools

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
            return function_signatures['RadiusOf'], 1.0
        elif words[index] == 'circle':
            return function_signatures['Circle'], 1.0
        elif words[index] == 'O':
            return FunctionSignature('O', 'modifier', []), 1.0
        elif words[index] == '5':
            return FunctionSignature('5', 'number', []), 1.0
        else:
            return None, 1.0


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
    pass

def bff1(binary_rule):
    """
    binary feature function version 1
    Usually, this will depend on unary feature function.

    :param binary_rule:
    :return:
    """
    pass

def get_possible_unary_rules(words, syntax_tree, tags, parent_index, parent_signature):
    """
    list of UnaryRule objects
    Need to enforce type-matching here!

    :param words:
    :param syntax_tree:
    :param tags:
    :param parent_index:
    :param parent_signature:
    :return:
    """
    return []

def get_possible_binary_rules(words, syntax_tree, tags, parent_index, parent_signature):
    """
    list of BinaryRule objects
    Need to enforce type-matching here! That is, get only rules with the ontology.
    (perhaps emove equivalent rules. For instance, equality. but this might be bad.. or add symmetry feature)

    :param words:
    :param syntax_tree:
    :param tags:
    :param parent_index:
    :param parent_signature:
    :return:
    """
    return []


class UnarySemanticModel(object):
    def __init__(self, unary_rules, unary_feature_function):
        self.unary_rules = unary_rules
        self.unary_feature_function = unary_feature_function

    def get_rule_distribution(self, words, syntax_tree, tags, parent_index, parent_signature):
        """
        dictionary of unary_rule : probability pair
        The distribution must be well defined, i.e. must sum up to 1.

        :param words:
        :param syntax:
        :param tags:
        :param parent_index:
        :param parent_signature:
        :return:
        """
        distribution = {}
        local_unary_rules = get_possible_binary_rules(words, syntax_tree, tags, parent_index, parent_signature)
        return distribution


class TopDownNaiveDecoder(object):
    def __init__(self, unary_semantic_model, binary_semantic_model):
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

        # TODO : incorporate probability (dictionary rather than list), enforce non-redundancy within formula
        # TODO : since this is top-down, no syntactic feature for implied functions. Reweight formulas in another method

        def _recurse_unary(unary_rule):
            assert isinstance(unary_rule, UnaryRule)
            if unary_rule.child_signature.is_leaf():
                child_nodes = [Node(unary_rule.child_signature, [])]
            elif unary_rule.child_signature.is_unary():
                next_unary_rules = get_possible_unary_rules(words, syntax_tree, tags,
                                                            unary_rule.child_index, unary_rule.child_signature)
                child_nodes = [_recurse_unary(next_unary_rule) for next_unary_rule in next_unary_rules]
            elif unary_rule.child_signature.is_binary():
                next_binary_rules = get_possible_binary_rules(words, syntax_tree, tags,
                                                              unary_rule.child_index, unary_rule.child_signature)
                child_nodes = [_recurse_binary(next_binary_rule) for next_binary_rule in next_binary_rules]

            parent_nodes = [Node(unary_rule.parent_signature, [child_node]) for child_node in child_nodes]
            return parent_nodes

        def _recurse_binary(binary_rule):
            assert isinstance(binary_rule, BinaryRule)
            if binary_rule.a_signature.is_leaf():
                a_nodes = [Node(binary_rule.a_signature, [])]
            elif binary_rule.a_signature.is_unary():
                next_unary_rules = get_possible_unary_rules(words, syntax_tree, tags,
                                                            binary_rule.a_index, binary_rule.a_signature)
                a_nodes = [_recurse_unary(next_unary_rule) for next_unary_rule in next_unary_rules]
            elif binary_rule.a_signature.is_binary():
                next_binary_rules = get_possible_binary_rules(words, syntax_tree, tags,
                                                              binary_rule.a_index, binary_rule.a_signature)
                a_nodes = [_recurse_unary(next_binary_rule) for next_binary_rule in next_binary_rules]

            if binary_rule.b_signature.is_leaf():
                b_nodes = [Node(binary_rule.b_signature, [])]
            elif binary_rule.b_signature.is_unary():
                next_unary_rules = get_possible_unary_rules(words, syntax_tree, tags,
                                                            binary_rule.b_index, binary_rule.b_signature)
                b_nodes = [_recurse_unary(next_unary_rule) for next_unary_rule in next_unary_rules]
            elif binary_rule.b_signature.is_binary():
                next_binary_rules = get_possible_binary_rules(words, syntax_tree, tags,
                                                              binary_rule.b_index, binary_rule.b_signature)
                b_nodes = [_recurse_unary(next_binary_rule) for next_binary_rule in next_binary_rules]

            parent_nodes = [Node(binary_rule.parent_signature, [a_node, b_node])
                            for a_node, b_node in itertools.product(a_nodes, b_nodes)]
            return parent_nodes

        start_unary_rules = get_possible_unary_rules(words, syntax_tree, tags, None, function_signatures['StartTruth'])
        nodes = itertools.chain(*[_recurse_unary(start_unary_rule) for start_unary_rule in start_unary_rules])


        return {}

