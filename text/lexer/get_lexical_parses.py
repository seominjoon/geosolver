from geosolver.text.lexer.separate_expressions import separate_expressions
from geosolver.text.lexer.states import LexicalParse
from geosolver.text.lexer.string_to_words import string_to_words
from geosolver.text.lexer.words_to_sentences import words_to_sentences

__author__ = 'minjoon'


def get_lexical_parses(string):
    words = string_to_words(string)
    sentences = words_to_sentences(words)
    lexical_parses = []
    for sentence in sentences:
        tokens, expression_parses = separate_expressions(sentence)
        lexical_parse = LexicalParse(tokens, expression_parses)
        lexical_parses.append(lexical_parse)
    return lexical_parses