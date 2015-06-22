import os

from geosolver.database.geoserver_interface import geoserver_interface
from geosolver.text.lexer.get_lexical_parses import get_lexical_parses
from geosolver.text.lexer.string_to_tokens import string_to_tokens
from geosolver.text.syntax.create_syntax import create_syntax
from geosolver.text.syntax.get_syntax_paths import get_syntax_paths
from geosolver.text.syntax.parsers import stanford_parser
from geosolver.utils.prep import get_number_string
from geosolver.text.syntax.states import SyntaxTree

__author__ = 'minjoon'


def test_stanford_parser():
    string = "A cat is walking."
    tokens = string_to_tokens(string)
    k = 3
    syntax_trees = stanford_parser.parse_syntax_trees(tokens, k)
    for syntax_tree in syntax_trees.values():
        assert isinstance(syntax_tree, SyntaxTree)
        print(syntax_tree.graph.nodes(data=True))
        syntax_tree.display_graph()


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


def test_trees():
    root_path = "/Users/minjoon/Desktop/questions2"
    if not os.path.exists(root_path):
        os.mkdir(root_path)
    k = 300
    numbers = [26, 28]
    questions = geoserver_interface.download_questions(numbers)
    for pk, question in questions.iteritems():
        folder_name = get_number_string(pk, 4)
        question_path = os.path.join(root_path, folder_name)
        if not os.path.exists(question_path):
            os.mkdir(question_path)
        lexical_parses = get_lexical_parses(question.text)
        for idx, lexical_parse in enumerate(lexical_parses):
            sentence_folder_name = get_number_string(idx, 2)
            sentence_path = os.path.join(question_path, sentence_folder_name)
            if not os.path.exists(sentence_path):
                os.mkdir(sentence_path)

            syntax = create_syntax(lexical_parse.tokens, k)
            syntax.save_graphs(sentence_path)
            print(pk, idx)



if __name__ == "__main__":
    test_stanford_parser()
    # test_syntax_path()
    # test_trees()