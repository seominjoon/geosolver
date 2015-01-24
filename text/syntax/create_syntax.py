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
    syntax_trees = stanford_parser.parse_syntax_trees(tokens, k)
    syntax = Syntax(tokens, syntax_trees)
    return syntax
