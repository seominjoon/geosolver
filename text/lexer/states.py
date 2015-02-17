__author__ = 'minjoon'


class Token(object):
    def __init__(self, sentence, index):
        self.sentence = sentence
        self.index = index
        self.word = sentence[index]
        self.label = "%s-%d" % (self.word, self.index)
        self.key = index

    def __repr__(self):
        return "%s(word=%r, index=%d)" % (self.__class__.__name__, self.word, self.index)

    def __eq__(self, other):
        assert isinstance(other, Token)
        return self.index == other.index


class ExpressionParse(object):
    def __init__(self, words, reference_idx):
        self.words = words
        self.reference_idx = reference_idx  # the token idx in sentence that the expression is replacing.

    def __repr__(self):
        return "%s(words=%r, idx=%d" % (self.__class__.__name__, self.words, self.reference_idx)


class LexicalParse(object):
    def __init__(self, tokens, expression_parses):
        self.tokens = tokens
        self.expression_parses = expression_parses