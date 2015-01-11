import networkx as nx

__author__ = 'minjoon'

class Type:
    def __init__(self, name, label=None):
        self.name = name
        self.id = hash(name)
        if label is None:
            self.label = self.name
        else:
            self.label = label


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


class Ontology:
    def __init__(self, types, symbols, inheritance_graph, ontology_graph):
        self.types = types
        self.symbols = symbols
        self.inheritance_graph = inheritance_graph
        self.ontology_graph = ontology_graph
