import networkx as nx
from geosolver.ontology.states import OntologyPath

__author__ = 'minjoon'


def get_ontology_paths(basic_ontology, from_type, to_obj):
    """
    to_obj can be either Type or Function

    :param ontology:
    :param from_type:
    :param to_obj:
    :return:
    """
    graph = basic_ontology.ontology_graph.copy()
    assert isinstance(graph, nx.DiGraph)

    for function in basic_ontology.functions.values():
        if function is not to_obj and function.valence > 1:
            graph.remove_node(function.id)

    if from_type is to_obj:
        paths = [cycle for cycle in nx.simple_cycles(basic_ontology.ontology_graph) if from_type.id in cycle]

    elif not nx.has_path(graph, from_type.id, to_obj.id):
        paths = []

    else:
        paths = nx.all_simple_paths(graph, from_type.id, to_obj.id)

    path_dict = {key: OntologyPath(basic_ontology, [basic_ontology.get_by_id(id_) for id_ in path], key)
                 for key, path in enumerate(paths)}
    return path_dict


