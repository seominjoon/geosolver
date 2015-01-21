"""
Create Syntax object
"""
from geosolver.text.syntax.parsers import stanford_parser
from geosolver.text.syntax.states import Syntax
__author__ = 'minjoon'


def create_syntax(tokens, k):
    """

    :param tuple tokens:
    :return Syntax:
    """
    pairs = stanford_parser.parse_tree_score_pairs(tokens, k)
    syntax = Syntax(tokens, pairs)
    return syntax
