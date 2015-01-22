__author__ = 'minjoon'


class AbstractToken(object):
    def __init__(self, name):
        self.name = name
        self.label = name


class Token(AbstractToken):
    def __init__(self, sentence, index):
        self.sentence = sentence
        self.index = index
        self.word = sentence[index]
        self.name = self.index
        self.label = "%s-%d" % (self.word, self.index)

    def __repr__(self):
        return "%s(word=%s, index=%d)" % (self.__class__.__name__, self.word, self.index)

