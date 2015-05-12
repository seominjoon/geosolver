from geosolver.text.ontology_states import FunctionSignature

__author__ = 'minjoon'


class TagRule(object):
    def __init__(self, words, syntax_tree, index, signature):
        self.words = words
        self.syntax_tree = syntax_tree
        self.index = index
        self.signature = signature

    def __repr__(self):
        if self.index is None:
            word = None
        else:
            word = self.words[self.index]
        return "%s@%r:%s" % (word, self.index, self.signature.name)

    def __eq__(self, other):
        return repr(self) == repr(other)

class SemanticRule(object):
    pass


class UnaryRule(SemanticRule):
    def __init__(self, words, syntax_tree, tag_model, parent_index, parent_signature, child_index, child_signature):
        assert isinstance(parent_signature, FunctionSignature)
        assert isinstance(child_signature, FunctionSignature)
        assert isinstance(parent_index, int) or parent_index is None
        assert isinstance(child_index, int) or child_index is None
        self.words = words
        self.syntax_tree = syntax_tree
        self.tag_model = tag_model
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


class BinaryRule(SemanticRule):
    def __init__(self, words, syntax_tree, tag_model,
                 parent_index, parent_signature, a_index, a_signature, b_index, b_signature):
        assert isinstance(parent_signature, FunctionSignature)
        assert isinstance(a_signature, FunctionSignature)
        assert isinstance(b_signature, FunctionSignature)
        assert isinstance(parent_index, int) or parent_index is None
        assert isinstance(a_index, int) or a_index is None
        assert isinstance(b_index, int) or b_index is None
        self.words = words
        self.syntax_tree = syntax_tree
        self.tag_model = tag_model
        self.parent_index = parent_index
        self.parent_signature = parent_signature
        self.a_index = a_index
        self.a_signature = a_signature
        self.b_index = b_index
        self.b_signature = b_signature
        self.a_rule = UnaryRule(words, syntax_tree, tag_model, parent_index, parent_signature, a_index, a_signature)
        self.b_rule = UnaryRule(words, syntax_tree, tag_model, parent_index, parent_signature, b_index, b_signature)
        self.c_rule = UnaryRule(words, syntax_tree, tag_model, a_index, a_signature, b_index, b_signature)
        self.unary_rules = [self.a_rule, self.b_rule, self.c_rule]

    def __hash__(self):
        return hash((self.parent_index, self.parent_signature,
                     self.a_index, self.a_signature, self.b_index, self.b_signature))

    def __repr__(self):
        return "%s@%r->%s@%r|%s@%r" % (self.parent_signature.name, self.parent_index,
                                       self.a_signature.name, self.a_index,
                                       self.b_signature.name, self.b_index)

    def __eq__(self, other):
        return repr(self) == repr(other)
