from geosolver.ontology.ontology_definitions import issubtype
from geosolver.text2.syntax_parser import SyntaxParse

__author__ = 'minjoon'

def _span_to_string(span):
    if span == "i":
        return span
    elif span[0] + 1 == span[1]:
        return "%d" % span[0]
    else:
        return "%d:%d" % (span[0], span[1]-1)

class TagRule(object):
    def __init__(self, syntax_parse, span, signature):
        assert isinstance(syntax_parse, SyntaxParse)
        self.syntax_parse = syntax_parse
        self.span = span
        self.signature = signature
        self.is_implicit = self.span == "i"
        self.string = "_".join(self.syntax_parse.words[i] for i in range(*self.span))

    def get_words(self):
        words = tuple(self.syntax_parse.words[idx] for idx in range(*self.span))
        return words

    def get_length(self):
        return self.span[1] - self.span[0]

    def is_single_word(self):
        return self.get_length() == 1

    def __hash__(self):
        return hash((self.span, self.signature))

    def __eq__(self, other):
        span = self.span == other.span
        sig = self.signature == other.signature
        return span and sig

    def __repr__(self):
        return "%s@%s[%s]" % (repr(self.signature.id), _span_to_string(self.span), self.string)

    def __hash__(self):
        return hash((self.span, self.signature))


class SemanticRule(object):
    pass

class UnaryRule(SemanticRule):
    def __init__(self, parent_tag_rule, child_tag_rule):
        assert UnaryRule.check_validity(parent_tag_rule, child_tag_rule)
        self.syntax_parse = parent_tag_rule.syntax_parse
        self.parent_tag_rule = parent_tag_rule
        self.child_tag_rule = child_tag_rule

    def __repr__(self):
        return "%r->%r" % (self.parent_tag_rule, self.child_tag_rule)

    def __hash__(self):
        return hash((self.parent_tag_rule, self.child_tag_rule))

    def __eq__(self, other):
        return self.parent_tag_rule == other.parent_tag_rule and self.child_tag_rule == other.child_tag_rule

    @staticmethod
    def check_validity(parent_tag_rule, child_tag_rule):
        valence = parent_tag_rule.signature.valence
        if valence == 0:
            return False
        elif valence == 1:
            return issubtype(child_tag_rule.signature.return_type, parent_tag_rule.signature.arg_types[0])
        elif valence == 2:
            return issubtype(child_tag_rule.signature.return_type, parent_tag_rule.signature.arg_types[0])
        raise Exception()





class BinaryRule(SemanticRule):
    def __init__(self, parent_tag_rule, child_a_tag_rule, child_b_tag_rule):
        assert BinaryRule.check_validity(parent_tag_rule, child_a_tag_rule, child_b_tag_rule)
        self.syntax_parse = parent_tag_rule.syntax_parse
        self.parent_tag_rule = parent_tag_rule
        self.child_a_tag_rule = child_a_tag_rule
        self.child_b_tag_rule = child_b_tag_rule

    @staticmethod
    def check_validity(parent_tag_rule, a_tag_rule, b_tag_rule):
        valence = parent_tag_rule.signature.valence
        if valence == 2:
            a = issubtype(a_tag_rule.signature.return_type, parent_tag_rule.signature.arg_types[0])
            b = issubtype(b_tag_rule.signature.return_type, parent_tag_rule.signature.arg_types[1])
            return a and b
        else:
            return False

    def __repr__(self):
        return "%r->%r|%r" % (self.parent_tag_rule, self.child_a_tag_rule, self.child_b_tag_rule)

    def __hash__(self):
        return hash((self.parent_tag_rule, self.child_a_tag_rule, self.child_b_tag_rule))

    def __eq__(self, other):
        return self.parent_tag_rule == other.parent_tag_rule and self.child_a_tag_rule == other.child_a_tag_rule and \
            self.child_b_tag_rule == other.child_b_tag_rule
