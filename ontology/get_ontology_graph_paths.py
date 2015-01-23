from geosolver.ontology.states import BasicOntology, Function
from geosolver.ontology.states import Type

import networkx as nx

__author__ = 'minjoon'


def get_ontology_graph_paths(basic_ontology, from_type, to_obj):
    """
    to_obj can be either Type or Function
    path is only counted from type to function.
    Function to type path is weighted 0.
    Ex. type number -> type line: 1, type number -> function line: 2

    :param ontology:
    :param from_type:
    :param to_obj:
    :return:
    """
    assert isinstance(basic_ontology, BasicOntology)
    graph = basic_ontology.ontology_graph.copy()
    assert isinstance(graph, nx.DiGraph)
    assert isinstance(from_type, Type)

    for function in basic_ontology.functions.values():
        if function is not to_obj and function.valence > 1:
            graph.remove_node(function.id)

    if from_type is to_obj:
        paths = [cycle for cycle in nx.simple_cycles(basic_ontology.ontology_graph) if from_type.id in cycle]

    elif not nx.has_path(graph, from_type.id, to_obj.id):
        paths = []

    else:
        paths = nx.all_simple_paths(graph, from_type.id, to_obj.id)

    proper_paths = tuple(tuple(basic_ontology.get_by_id(id_) for id_ in path) for path in paths)
    return proper_paths


