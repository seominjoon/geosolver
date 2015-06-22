import networkx as nx

from geosolver.ontology import shared
from geosolver.utils.prep import display_graph

__author__ = 'minjoon'


class Type(object):
    def __init__(self, name, supertype=None, label=None):
        assert isinstance(name, str)

        self.name = name  # Intra-class identifier
        self.key = name
        self.id = (self.__class__, name)  # Inter-class identifier
        self.supertype = supertype
        if label is None:
            self.label = self.name
        else:
            self.label = label

    def has_supertype(self):
        return self.supertype is not None

    def __eq__(self, other):
        return self.id == other.id

    def __repr__(self):
        return "%s(name='%s')" % (self.__class__.__name__, self.name)


class Function(object):
    def __init__(self, name, arg_types, return_type, label=None):
        for type_ in arg_types:
            assert isinstance(type_, Type)
        assert isinstance(return_type, Type)

        self.name = name
        self.key = name
        self.arg_types = arg_types
        self.return_type = return_type
        self.type = return_type
        self.id = (self.__class__, name)
        self.valence = len(self.arg_types)
        if label is None:
            self.label = name
        else:
            self.label = label

        assert isinstance(self.label, str)

    def __eq__(self, other):
        return self.id == other.id

    def __repr__(self):
        return "%s(%r, return_type=%r)" % (self.__class__.__name__, self.label, self.return_type.name)


class Constant(object):
    def __init__(self, content, type_, label=None):
        self.content = content
        self.key = content
        self.id = content
        self.type = type_
        if label is None:
            label = "%s:%r" % (self.type.name, self.key)
        self.label = label

    def __eq__(self, other):
        return self.content == other.content

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, self.content)



class Formula(object):
    def __init__(self, basic_ontology, current, children):
        assert isinstance(basic_ontology, BasicOntology)
        assert isinstance(current, Function) or isinstance(current, Constant)
        self.basic_ontolgy = basic_ontology
        self.current = current
        self.children = children

    def __repr__(self):
        if len(self.children) == 0:
            return self.current.label
        else:
            return "%s(%s)" % (self.current.name, ", ".join(repr(child) for child in self.children))

class BasicOntology(object):
    """
    Basic ontology defines the functions, their symbols (names), and what arguments they take in / return.
    """
    def __init__(self, types, functions, inheritance_graph, ontology_graph):
        assert isinstance(types, dict)
        assert isinstance(functions, dict)
        assert isinstance(inheritance_graph, nx.DiGraph)
        assert isinstance(ontology_graph, nx.DiGraph)

        self.types = types
        self.functions = functions
        self.inheritance_graph = inheritance_graph
        self.ontology_graph = ontology_graph
        self.types_by_id = {type_.id: type_ for type_ in self.types.values()}
        self.functions_by_id = {function.id: function for function in self.functions.values()}

    def isinstance(self, type0, type1):
        """
        Returns True if type0 is instance of type1

        :param Type type0:
        :param Type type1:
        :return bool:
        """
        return shared.isinstance_(self.inheritance_graph, type0, type1)

    def display_ontology_graph(self):
        display_graph(self.ontology_graph)

    def get_by_id(self, id_):
        class_name, name = id_
        if class_name == Type:
            return self.types[name]
        elif class_name == Function:
            return self.functions[name]
        else:
            raise Exception(class_name)

    def __repr__(self):
        return "%s(len(type_defs)=%d, len(function_defs)=%d)" % (self.__class__.__name__, len(self.types), len(self.functions))


class OntologyPath(object):
    def __init__(self, basic_ontology, path_nodes, key):
        self.basic_ontology = basic_ontology
        self.path_nodes = path_nodes
        self.key = key
        self.id = (path_nodes[0].id, path_nodes[-1].id, key)

    def __repr__(self):
        return "%s(key=%d, path=[%s])" % (self.__class__.__name__, self.key,
                                          ", ".join(node.key for node in self.path_nodes))

    def __len__(self):
        return len(self.path_nodes)


class OntologySemantics(object):
    """
    Contains sematnic information of the ontolgy.
    For instance, evaluation of constant function such as "5",
    or what a formula means algebraically.
    """
    def __init__(self):
        pass


class Truth(object):
    """
    Value indicates the truth-ness,
    being certain if 0 or less and uncertain if positive.
    Sigma is the rough prediction of the variance of the expression.

    For instance, we might assign 100% probability for expression <= 0,
    and 0% (or 50%; it doesn't really matter) probability for expression >= sigma.
    We can linearly interpolate in the middle.

    For concrete example, see 'equal' function in function_definitions.
    """
    def __init__(self, value, sigma):
        self.value = value
        self.sigma = sigma

