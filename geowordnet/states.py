from collections import namedtuple
from geosolver.ontology.states import BasicOntology

__author__ = 'minjoon'


class Entry(object):
    def __init__(self, lemma, pos, function):
        self.lemma = lemma
        self.pos = pos
        self.function = function

    def __repr__(self):
        return "%s(lemma=%s, pos=%s, function=%s)" % (self.__class__.__name__, self.lemma, self.pos, self.function.name)


class GeoWordNet(object):
    """
    When given word, we want to find the closest lemma, and
    """
    def __init__(self, entries, basic_ontology):
        for entry in entries:
            assert isinstance(entry, Entry)

        self.entries = entries
        self.basic_ontology = basic_ontology

EntryScorePair = namedtuple('EntryScorePair', 'entry score')
FunctionScorePair = namedtuple('FunctionScorePair', 'function score')
ConstantScorePair = namedtuple('ConstantScorePair', 'constant score')

