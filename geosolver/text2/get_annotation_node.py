from collections import deque
import re
from pyparsing import *
from geosolver.text2.ontology import function_signatures, FunctionSignature, VariableSignature
from geosolver.text2.rule import TagRule

__author__ = 'minjoon'

class AnnotationNode(object):
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


def get_annotation_node(syntax_parse, annotation_string):
    words = syntax_parse.words
    def span_f(a, b, c):
        if len(c) == 1:
            if c[0] == 'i':
                return 'i'
            else:
                return int(c[0]), int(c[0])+1
        else:
            return int(c[0]), int(c[1])+1

    def tag_f(a, b, c):
        assert len(c) == 1
        if c[0][0].isupper() or re.match('^\d+(\.\d+)?', c[0][0]):
            return 'function', c[0]
        else:
            return 'variable', c[0]

    def expr_f(a, b, c):
        local_span = c[1]
        children = c[2:]
        type_, s = c[0]
        name = "_".join(words[idx] for idx in range(*local_span))
        if s in function_signatures:
            signature = function_signatures[s]
        elif type_ == 'function' and len(children) == 0:
            signature = FunctionSignature(local_span, s, [], name=name)
        elif type_ == 'variable' and len(children) == 0:
            signature = VariableSignature(local_span, s, name=name)
        else:
            raise Exception()
        content = TagRule(syntax_parse, local_span, signature)
        return AnnotationNode(content, children)

    current = Word(alphanums)
    span = (Word(nums) + Literal(":").suppress() + Word(nums)) | Word(nums)
    string = Literal("[").suppress() + Word(alphanums+"_") + Literal("]").suppress()
    tag = current.setParseAction(tag_f) + Literal("@").suppress() + span.setParseAction(span_f) + Optional(string).suppress()
    expr = Forward()
    expr << (tag + Optional(Literal("(").suppress() + expr +
                           ZeroOrMore(Literal(",").suppress() + expr) + Literal(")").suppress()))
    tokens = expr.setParseAction(expr_f).parseString(annotation_string)
    return tokens[0]

def is_valid_annotation(syntax_parse, annotation_string):
    try:
        get_annotation_node(syntax_parse, annotation_string)
        return True
    except:
        return False





