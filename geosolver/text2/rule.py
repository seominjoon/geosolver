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
    def __init__(self, syntax_parse, parent_tag_rule, child_tag_rule):
        self.syntax_parse = syntax_parse
        self.parent_tag_rule = parent_tag_rule
        self.child_tag_rule = child_tag_rule

    def __repr__(self):
        return "%r->%r" % (self.parent_tag_rule, self.child_tag_rule)


class IsRule(SemanticRule):
    def __init__(self, syntax_parse, a_tag_rule, b_tag_rule):
        self.syntax_parse = syntax_parse
        self.a_tag_rule = a_tag_rule
        self.b_tag_rule = b_tag_rule

    def __repr__(self):
        return "%r~%r" % (self.a_tag_rule, self.b_tag_rule)

class ConjRule(SemanticRule):
    def __init__(self, syntax_parse, a_tag_rule, b_tag_rule):
        self.syntax_parse =syntax_parse
        self.a_tag_rule = a_tag_rule
        self.b_tag_rule = b_tag_rule

    def __repr__(self):
        return "%r^%r" % (self.a_tag_rule, self.b_tag_rule)


class BinaryRule(SemanticRule):
    def __init__(self, syntax_parse, parent_tag_rule, child_a_tag_rule, child_b_tag_rule):
        self.syntax_parse = syntax_parse
        self.parent_tag_rule = parent_tag_rule
        self.child_a_tag_rule = child_a_tag_rule
        self.child_b_tag_rule = child_b_tag_rule

    def __repr__(self):
        return "%r->%r|%r" % (self.parent_tag_rule, self.child_a_tag_rule, self.child_b_tag_rule)


class ImplicationRule(SemanticRule):
    def __init__(self, syntax_parse, parent_tag_rule, arg_idx, implied_tag_rules, child_tag_rule):
        self.syntax_parse = syntax_parse
        self.parent_tag_rule = parent_tag_rule
        self.arg_idx = arg_idx
        self.implied_tag_rules = implied_tag_rules
        self.child_tag_rule = child_tag_rule

    def __repr__(self):
        implied_string = "".join([repr(implied_tag_rule) + ">>" for implied_tag_rule in self.implied_tag_rules])
        return "%r,%d->%s%r" % (self.parent_tag_rule, self.arg_idx, implied_string, self.child_tag_rule)