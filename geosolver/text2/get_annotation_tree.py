from collections import deque
from pyparsing import *
from geosolver.text2.ontology import function_signatures, issubtype, FunctionSignature, Variable, Span

__author__ = 'minjoon'

class AnnotationNode(object):
    def __init__(self, content, span, children):
        assert content.valence >= len(children)
        self.content = content
        self.span = span
        self.children = children

    def __repr__(self):
        if self.span == "i":
            span_string = self.span
        elif self.span[0] + 1 == self.span[1]:
            span_string = "%d" % self.span[0]
        else:
            span_string = "%d:%d" % self.span

        if len(self.children) == 0:
            return "%s@%s" % (self.content.name, span_string)
        else:
            args_string = ", ".join(repr(child) for child in self.children)
            return "%s@%s(%s)" % (self.content.name, span_string, args_string)


class AnnotationTree(object):
    def __init__(self, words, head):
        self.words = words
        self.head = head

    def __iter__(self):
        queue = deque()
        queue.appendleft(self.head)
        while len(queue) > 0:
            current = queue.pop()
            for child in current.children:
                queue.appendleft(child)
            yield current

    def __repr__(self):
        return repr(self.head)



def get_annotation_tree(words, annotation_string):
    def span_f(a, b, c):
        if len(c) == 1:
            if c[0] == 'i':
                return 'i'
            else:
                return int(c[0]), int(c[0])+1
        else:
            return int(c[0]), int(c[1])

    def tag_f(a, b, c):
        if len(c) == 1:
            return 'function', c[0]
        else:
            return 'variable', c[1]

    def expr_f(a, b, c):
        local_span = c[1]
        children = c[2:]
        type_, string = c[0]
        if local_span == "i":
            name = string
        else:
            name = "_".join(words[idx] for idx in range(*local_span))
        if string in function_signatures:
            content = function_signatures[string]
        elif type_ == 'function' and len(children) == 0:
            content = FunctionSignature(local_span, string, [], name=string)
        else:
            content = Variable(local_span, string, name="$" + string)
        return AnnotationNode(content, local_span, children)

    current = Optional(Literal("$")) + Word(alphas)
    span = Literal("i") | (Word(nums) + Literal(":").suppress() + Word(nums)) | Word(nums)
    tag = current.setParseAction(tag_f) + Literal("@").suppress() + span.setParseAction(span_f)
    expr = Forward()
    expr << (tag + Optional(Literal("(").suppress() + expr +
                           ZeroOrMore(Literal(",").suppress() + expr) + Literal(")").suppress()))
    tokens = expr.setParseAction(expr_f).parseString(annotation_string)
    return AnnotationTree(words, tokens[0])


def is_valid_annotation(words, annotation_string):
    try:
        get_annotation_tree(words, annotation_string)
        return True

    except:
        return False





