import itertools
import networkx as nx
from geosolver.ontology.sanity_check import basic_sanity_check
from geosolver.ontology.states import Type, Function, BasicOntology
from geosolver.ontology.shared import isinstance_

__author__ = 'minjoon'


def load_ontology(type_defs, symbol_defs):
    """
    Load basic_ontology object from type and function definitions (raw string dict).
    First checks the sanity of the definitions, and then induce Type and FunctionNode objects.
    Lastly, construct inheritance graph for type and basic_ontology graph.

    :param dict type_defs:
    :param dict symbol_defs:
    :return Ontology:
    """
    basic_sanity_check(type_defs, symbol_defs)

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
        symbol_ = Function(symbol_def['name'], arg_types, return_type, label=label)
        symbols[symbol_.name] = symbol_

    inheritance_graph = _construct_inheritance_graph(types)
    ontology_graph = _construct_ontology_graph(types, inheritance_graph, symbols)
    ontology = BasicOntology(types, symbols, inheritance_graph, ontology_graph)
    return ontology


def _construct_inheritance_graph(types):
    """
    Inheritance graph draws an edge from a supertype to subtype.
    For instance, circle is a subtype of entity, so an edge is drawn from entity to circle.
    this information is used for type grounding when constructing basic_ontology graph.
    The node is indexed by the name of the type.

    :param dict type_defs:
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


def _construct_ontology_graph(types, inheritance_graph, functions):
    assert isinstance(types, dict)
    assert isinstance(functions, dict)

    graph = nx.DiGraph()

    for function in functions.values():
        assert isinstance(function, Function)
        for type_ in types.values():
            assert isinstance(type_, Type)
            # from type edges: if type is supertype of function's return type,
            # or function's return type is instance of type
            if isinstance_(inheritance_graph, function.return_type, type_):
            # if function.return_type == type_:
                graph.add_edge(type_.id, function.id)

            # to type edges: if type is instance of function's arg type
            for arg_idx, arg_type in enumerate(function.arg_types):
                # if isinstance_(inheritance_graph, type_, arg_type):
                if type_ == arg_type:
                    graph.add_edge(function.id, type_.id, label=arg_idx, arg_idx=arg_idx)

    return graph