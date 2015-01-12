import networkx as nx

__author__ = 'minjoon'


class Type:
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


class Symbol:
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


class Ontology:
    def __init__(self, types, symbols, inheritance_graph, ontology_graph):
        assert isinstance(inheritance_graph, nx.DiGraph)
        assert isinstance(ontology_graph, nx.MultiDiGraph)

        self.types = types
        self.symbols = symbols
        self.inheritance_graph = inheritance_graph
        self.ontology_graph = ontology_graph
