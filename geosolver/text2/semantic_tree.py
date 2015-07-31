from collections import deque
from geosolver.ontology.ontology_definitions import FormulaNode
from geosolver.text2.rule import UnaryRule, BinaryRule

__author__ = 'minjoon'


class SemanticTreeNode(object):
    def __init__(self, content, children):
        self.syntax_parse = content.syntax_parse
        self.content = content
        self.children = children
        self.valence = len(children)

    def __repr__(self):
        if len(self.children) == 0:
            return repr(self.content)
        else:
            args_string = ", ".join(repr(child) for child in self.children)
            return "%r(%s)" % (self.content, args_string)

    def __iter__(self):
        queue = deque()
        queue.appendleft(self)
        while len(queue) > 0:
            current = queue.pop()
            for child in current.children:
                queue.appendleft(child)
            yield current

    def is_leaf(self):
        return len(self.children) == 0

    def is_unary(self):
        return len(self.children) == 1

    def is_binary(self):
        return len(self.children) == 2

    def to_formula(self):
        args = [child.to_formula() for child in self.children]
        return FormulaNode(self.content.signature, args)

    def get_tag_rules(self):
        tag_rules = [node.content for node in self]
        return tag_rules

    def get_unary_rules(self):
        unary_rules = []
        for node in self:
            if node.is_unary():
                unary_rule = UnaryRule(self.content, self.children[0].content)
                unary_rules.append(unary_rule)

    def get_binary_rules(self):
        binary_rules = []
        for node in self:
            if node.is_binary():
                binary_rule = BinaryRule(self.content, self.children[0].content, self.children[1].content)
                binary_rules.append(binary_rule)
