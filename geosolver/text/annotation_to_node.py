import re
from pyparsing import *
from geosolver.text.node import Node
from geosolver.text.ontology import function_signatures, issubtype
from geosolver.text.ontology_states import FunctionSignature

__author__ = 'minjoon'

def is_valid_annotation(annotation):
    try:
        annotation_to_node(annotation)
        return True
    except:
        return False

def annotation_to_node(annotation):
    """
    Equal@i(RadiusOf@2(Circle@1('O'@0)), [5]@3)
    :param annotation:
    :return:
    """
    ref = Literal("'") + Word(alphanums, alphanums+"_") + Literal("'").suppress()
    var = Literal("<") + Word(alphas, alphanums+"_") + Literal(">").suppress()
    num = Literal("[") + Word(nums) + Literal("]").suppress()
    idx = Literal("i") | Word(nums)
    tag = (ref | var | num | Word(alphas)) + Literal("@").suppress() + idx
    expr = Forward()
    expr << tag + Optional(Literal("(").suppress() + expr + Optional(Literal(",").suppress() + expr) + Literal(")").suppress())
    tokens = expr.parseString(annotation)


    def _recurse(token_index):
        if tokens[token_index] == "'":
            token_index += 1
            function_signature = FunctionSignature(tokens[token_index], "modifier", [])
        elif tokens[token_index] == "<":
            token_index += 1
            function_signature = FunctionSignature(tokens[token_index], "variable", [])
        elif tokens[token_index] == "[":
            token_index += 1
            function_signature = FunctionSignature(tokens[token_index], "number", [])
        else:
            function_signature = function_signatures[tokens[token_index]]
        word_index = tokens[token_index+1]
        if word_index == 'i':
            word_index = None
        else:
            assert re.match(r"^\d+$", word_index)
            word_index = int(word_index)
        if function_signature.is_leaf():
            return token_index+2, Node(word_index, function_signature, [])

        elif function_signature.is_unary():
            end_index, node = _recurse(token_index+2)
            return end_index, Node(word_index, function_signature, [node])

        elif function_signature.is_binary():
            end_index, a_node = _recurse(token_index+2)
            end_index, b_node = _recurse(end_index)
            return end_index, Node(word_index, function_signature, [a_node, b_node])

    child_node = _recurse(0)[1]
    if issubtype(child_node.function_signature.return_type, 'truth'):
        parent_node = Node(None, function_signatures['StartTruth'], [child_node])
    else:
        raise Exception
    return parent_node

