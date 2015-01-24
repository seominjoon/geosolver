from geosolver.text.lexer.string_to_tokens import string_to_tokens
from geosolver.text.syntax.create_syntax import create_syntax
from geosolver.text.syntax.get_syntax_distance import get_syntax_distance
from geosolver.text.syntax.parsers import stanford_parser
from geosolver.utils import display_graph

__author__ = 'minjoon'


def test_stanford_parser():
    string = "A cat is walking."
    tokens = string_to_tokens(string)
    k = 3
    pairs = stanford_parser.parse_tree_score_pairs(tokens, 3)
    for tree, score in pairs:
        print(tree.nodes(data=True))
        display_graph(tree)


def test_create_syntax():
    string = "Line AB is perpendicular to CD."
    tokens = string_to_tokens(string)
    k = 5
    syntax = create_syntax(tokens, k)
    syntax.display_graphs()


def test_syntax_distance():
    string = "Line AB is perpendicular to CD."
    tokens = string_to_tokens(string)
    k = 5
    syntax = create_syntax(tokens, k)
    from_token = tokens[0]
    to_token = tokens[5]
    score = get_syntax_distance(syntax, from_token, to_token)
    print("%s to %s: %f" % (from_token.word, to_token.word, score))
    display_graph(syntax.syntax_graph_score_pairs[0].tree)


if __name__ == "__main__":
    test_syntax_distance()