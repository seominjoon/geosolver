from collections import namedtuple
from geosolver.geowordnet import filters
from geosolver.geowordnet.entry_proximity_score import entry_proximity_score
from geosolver.ontology.states import BasicOntology

__author__ = 'minjoon'


class Entry(object):
    def __init__(self, lemma, pos, symbol):
        self.lemma = lemma
        self.pos = pos
        self.symbol = symbol

    def proximity_score(self, word):
        return entry_proximity_score(word, self)

    def __repr__(self):
        return "%s(lemma=%s, pos=%s, symbol=%s)" % (self.__class__.__name__, self.lemma, self.pos, self.symbol.name)


class GeoWordNet(object):
    """
    When given word, we want to find the closest lemma, and
    """
    def __init__(self, entries, basic_ontology):
        for entry in entries:
            assert isinstance(entry, Entry)
        assert isinstance(basic_ontology, BasicOntology)

        self.entries = entries
        self.basic_ontology = basic_ontology

    def filter_entries(self, word, threshold):
        return filters.filter_entries(self, word, threshold)

    def filter_symbols(self, word, threshold):
        return filters.filter_symbols(self, word, threshold)

EntryScorePair = namedtuple('EntryScorePair', 'entry score')
SymbolScorePair = namedtuple('SymbolScorePair', 'symbol score')
