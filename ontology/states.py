import networkx as nx
from geosolver.ontology import shared
from geosolver.ontology.ontology_proximity_score import ontology_proximity_score

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


class Function(object):
    def __init__(self, name, arg_types, return_type, label=None):
        assert isinstance(name, str)
        for type_ in arg_types:
            assert isinstance(type_, Type)
        assert isinstance(return_type, Type)

        self.name = name
        self.arg_types = arg_types
        self.return_type = return_type
        self.id = hash(self.name)
        self.valence = len(self.arg_types)
        if label is None:
            self.label = name
        else:
            self.label = label

    def __repr__(self):
        return "%s(name='%s', return_type='%s')" % (self.__class__.__name__, self.name, self.return_type.name)


class Formula(object):
    pass


class BasicOntology(object):
    """
    Basic ontology defines the functions, their symbols (names), and what arguments they take in / return.
    """
    def __init__(self, types, functions, inheritance_graph, ontology_graph):
        assert isinstance(types, dict)
        assert isinstance(functions, dict)
        assert isinstance(inheritance_graph, nx.DiGraph)
        assert isinstance(ontology_graph, nx.MultiDiGraph)

        self.types = types
        self.functions = functions
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

    def __repr__(self):
        return "%s(len(type_defs)=%d, len(function_defs)=%d)" % (self.__class__.__name__, len(self.types), len(self.functions))


class OntologySemantics(object):
    """
    Contains sematnic information of the ontolgy.
    For instance, evaluation of constant function such as "5",
    or what a formula means algebraically.
    """
    pass