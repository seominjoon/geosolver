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

    def __repr__(self):
        return "%s@%s[%s]" % (repr(self.signature), _span_to_string(self.span), self.string)

    def __hash__(self):
        return hash((self.span, self.signature))


class SemanticRule(object):
    pass

class UnaryRule(SemanticRule):
    def __init__(self, parent_tag_rule, child_tag_rule):
        self.syntax_parse = parent_tag_rule.syntax_parse
        self.parent_tag_rule = parent_tag_rule
        self.child_tag_rule = child_tag_rule

    def __repr__(self):
        return "%r->%r" % (self.parent_tag_rule, self.child_tag_rule)


class BinaryRule(SemanticRule):
    def __init__(self, parent_tag_rule, child_a_tag_rule, child_b_tag_rule):
        self.syntax_parse = parent_tag_rule.syntax_parse
        self.parent_tag_rule = parent_tag_rule
        self.child_a_tag_rule = child_a_tag_rule
        self.child_b_tag_rule = child_b_tag_rule

    def __repr__(self):
        return "%r->%r|%r" % (self.parent_tag_rule, self.child_a_tag_rule, self.child_b_tag_rule)
