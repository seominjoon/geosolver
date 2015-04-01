from geosolver.text.lexer.separate_expressions import separate_expressions
from geosolver.text.lexer.string_to_tokens import string_to_tokens
from geosolver.text.lexer.string_to_words import string_to_words
from geosolver.text.lexer.words_to_sentences import words_to_sentences

__author__ = 'minjoon'


def test_string_to_tokens():
    string = "If line AB = 3, then what is x+5?"
    print(string_to_tokens(string))


def test_separate_sentence_and_equations():
    string = "Line AB = CD. What is its length?"
    words = string_to_words(string)
    sentences = words_to_sentences(words)
    print(sentences)
    for sentence in sentences:
        print(separate_expressions(sentence))

if __name__ == "__main__":
    # test_string_to_tokens()
    test_separate_sentence_and_equations()

