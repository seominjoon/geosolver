__author__ = 'minjoon'

def _span_to_string(span):
    if span == "i":
        return span
    elif span[0] + 1 == span[1]:
        return "%d" % span[0]
    else:
        return "%d:%d" % span

class TagRule(object):
    def __init__(self, syntax_parse, span, signature):
        self.syntax_parse = syntax_parse
        self.span = span
        self.signature = signature
        self.is_implicit = self.span == "i"

    def __repr__(self):
        return "%s@%s" % (self.signature.name, _span_to_string(self.span))

class SemanticRule(object):
    pass

class UnaryRule(SemanticRule):
    def __init__(self, syntax_parse, a_tag_rule, b_tag_rule):
        self.syntax_parse = syntax_parse
        self.a_tag_rule = a_tag_rule
        self.b_tag_rule = b_tag_rule

    def __repr__(self):
        return "%r -> %r" % (self.a_tag_rule, self.b_tag_rule)


class IsRule(UnaryRule):
    def __repr__(self):
        return "%r ~ %r" % (self.a_tag_rule, self.b_tag_rule)

class ConjRule(UnaryRule):
    def __repr__(self):
        return "%r ^ %r" % (self.a_tag_rule, self.b_tag_rule)


class BinaryRule(SemanticRule):
    def __init__(self, syntax_parse, a_tag_rule, b_tag_rule, c_tag_rule):
        self.syntax_parse = syntax_parse
        self.a_tag_rule = a_tag_rule
        self.b_tag_rule = b_tag_rule
        self.c_tag_rule = c_tag_rule

    def __repr__(self):
        return "%r -> %r, %r" % (self.a_tag_rule, self.b_tag_rule, self.c_tag_rule)