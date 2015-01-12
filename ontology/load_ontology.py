import itertools
import networkx as nx
from geosolver.ontology.sanity_check import sanity_check
from geosolver.ontology.states import Type, Symbol, Ontology
from geosolver.ontology import definitions
from geosolver.ontology.shared import isinstance_

__author__ = 'minjoon'


def load_ontology(type_defs, symbol_defs):
    """
    Load ontology object from type and symbol definitions (raw string dict).
    First checks the sanity of the definitions, and then induce Type and Symbol objects.
    Lastly, construct inheritance graph for type and ontology graph.

    :param dict type_defs:
    :param dict symbol_defs:
    :return Ontology:
    """
    sanity_check(type_defs, symbol_defs)

    types = {}
    for type_def in type_defs:
        name = type_def['name']
        if 'supertype' in type_def:
            supertype = types[type_def['supertype']]
        else:
            supertype = None
        if 'label' in type_def:
            label = type_def['label']
        else:
            label = None
        type_ = Type(name, supertype=supertype, label=label)
        types[name] = type_

    symbols = {}
    for symbol_def in symbol_defs:
        arg_types = [types[arg_type_def] for arg_type_def in symbol_def['arg_types']]
        return_type = types[symbol_def['return_type']]
        if 'label' in symbol_def:
            label = symbol_def['label']
        else:
            label = None
        symbol_ = Symbol(symbol_def['name'], symbol_def['lemma'], arg_types, return_type, label=label)
        symbols[symbol_.name] = symbol_

    inheritance_graph = _construct_inheritance_graph(types)
    ontology_graph = _construct_ontology_graph(inheritance_graph, symbols)
    ontology = Ontology(types, symbols, inheritance_graph, ontology_graph)
    return ontology


def _construct_inheritance_graph(types):
    """
    Inheritance graph draws an edge from a supertype to subtype.
    For instance, circle is a subtype of entity, so an edge is drawn from entity to circle.
    this information is used for type matching when constructing ontology graph.
    The node is indexed by the name of the type.

    :param dict types:
    :return nx.DiGraph:
    """
    graph = nx.DiGraph()
    for type_ in types.values():
        assert isinstance(type_, Type)
        if type_.name not in graph.nodes():
            graph.add_node(type_.name, label=type_.label)
        if type_.has_supertype():
            graph.add_edge(type_.supertype.name, type_.name)

    return graph


def _construct_ontology_graph(inheritance_graph, symbols):
    """

    :param nx.DiGraph inheritance_graph:
    :param dict symbols:
    :return nx.DiGraph:
    """
    graph = nx.MultiDiGraph()

    for symbol0, symbol1 in itertools.product(symbols.values(), repeat=2):
        '''
        Add edge from symbol0 to symbol1 if one of symbol0's arg type matches return type of symbol1
        '''
        assert isinstance(symbol0, Symbol)
        assert isinstance(symbol1, Symbol)
        for idx, arg_type in enumerate(symbol0.arg_types):
            if isinstance_(inheritance_graph, symbol1.return_type, arg_type):
                '''
                If symbol1's return type is an instance of arg type, then create an edge.
                Ex. symbol1 return type is line, and arg type is entity.
                '''
                # key is set to idx, which means the edge is for idx'th argument of symbol0
                graph.add_edge(symbol0.name, symbol1.name, key=idx, arg_idx=idx, label=idx)

    return graph


if __name__ == "__main__":
    o = load_ontology(definitions.types, definitions.symbols)
    print(o)
    print(o.inheritance_graph.edges())
    print(o.ontology_graph.edges(data=True))
