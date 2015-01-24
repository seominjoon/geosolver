from geosolver.text.lexer.string_to_tokens import string_to_tokens
from geosolver.text.syntax.create_syntax import create_syntax
from geosolver.text.syntax.get_syntax_paths import get_syntax_paths
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


def test_syntax_path():
    string = "Line AB is perpendicular to CD."
    tokens = string_to_tokens(string)
    k = 5
    syntax = create_syntax(tokens, k)
    from_token = tokens[0]
    to_token = tokens[5]
    paths = get_syntax_paths(syntax, from_token, to_token)
    print([len(path) for path in paths.values()])
    syntax.syntax_trees[0].display_graph()


if __name__ == "__main__":
    test_syntax_path()