import networkx as nx
from geosolver.ontology import shared
from geosolver.ontology.symbol_proximity_score import symbol_proximity_score

__author__ = 'minjoon'


class Type(object):
    def __init__(self, name, supertype=None, label=None):
        assert isinstance(name, str)

        self.name = name
        self.id = hash(name)
        self.supertype = supertype
        if label is None:
            self.label = self.name
        else:
            self.label = label

    def has_supertype(self):
        return self.supertype is not None

    def __repr__(self):
        return "%s(name='%s')" % (self.__class__.__name__, self.name)


class Symbol(object):
    def __init__(self, name, lemma, arg_types, return_type, label=None):
        self.name = name
        self.lemma = lemma
        self.arg_types = arg_types
        self.return_type = return_type
        self.id = hash(self.name)
        self.valence = len(self.arg_types)
        if label is None:
            self.label = name
        else:
            self.label = label

    def __repr__(self):
        return "%s(name='%s', lemma='%s')" % (self.__class__.__name__, self.name, self.lemma)


class Ontology(object):
    def __init__(self, types, symbols, inheritance_graph, ontology_graph):
        assert isinstance(types, dict)
        assert isinstance(symbols, dict)
        assert isinstance(inheritance_graph, nx.DiGraph)
        assert isinstance(ontology_graph, nx.MultiDiGraph)

        self.types = types
        self.symbols = symbols
        self.inheritance_graph = inheritance_graph
        self.ontology_graph = ontology_graph

    def isinstance(self, type0, type1):
        """
        Returns True if type0 is instance of type1

        :param Type type0:
        :param Type type1:
        :return bool:
        """
        return shared.isinstance_(self.inheritance_graph, type0, type1)

    def symbol_proximity_score(self, from_symbol, to_symbol):
        """
        Returns the proximity from from_symbol to to_symbol.

        :param Symbol from_symbol:
        :param Symbol to_symbol:
        :return float:
        """
        return symbol_proximity_score(self, from_symbol, to_symbol)

    def __repr__(self):
        return "%s(len(types)=%d, len(symbols)=%d)" % (self.__class__.__name__, len(self.types), len(self.symbols))