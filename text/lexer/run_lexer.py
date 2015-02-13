from geosolver.text.lexer.separate_sentence_and_equations import separate_sentence_and_equations
from geosolver.text.lexer.string_to_tokens import string_to_tokens

__author__ = 'minjoon'


def test_string_to_tokens():
    string = "If line AB = 3, then what is x+5?"
    print(string_to_tokens(string))


def test_separate_sentence_and_equations():
    string = "If line AB = 3, then what is x+5?"
    print(separate_sentence_and_equations(string))

if __name__ == "__main__":
    # test_string_to_tokens()
    test_separate_sentence_and_equations()

