import networkx as nx
import numpy as np

__author__ = 'minjoon'


def ontology_proximity_score(ontology, from_function, to_function, arg_idx):
    """
    Given two function_defs, returns the proximity of to_function from from_function.
    For now, returns the inverse of the shortest distance from from_function to to_function
    If from_function and to_function are the same,
    then for the score to be non-zero, there has to exist a cycle.

    :param geosolver.basic_ontology.states.Ontology basic_ontology:
    :param geosolver.basic_ontology.states.Function from_function:
    :param geosolver.basic_ontology.states.Function to_function:
    :param int arg_idx:
    :return float:
    """
    # Restrict accessing ground without instantiated function.
    # (Instantiated function cannot be implied without diagram's help)
    if to_function.name == 'ground' and ontology.types['ground'] not in from_function.arg_types:
        return 0


    graph = ontology.ontology_graph.copy()
    assert isinstance(graph, nx.MultiDiGraph)

    for from_function_name, to_function_name, data in graph.edges(data=True):
        if graph.has_node(from_function_name):
            if from_function.name == from_function_name:
                """
                If the arg_idx of data != arg_idx, remove the edge (key=arg_idx)
                """
                if data['arg_idx'] != arg_idx:
                    graph.remove_edge(from_function_name, to_function_name, key=arg_idx)
            else:
                """
                If from_function has multiple arguments, then remove this function from the graph.
                """
                curr_from_function = ontology.functions[from_function_name]
                if curr_from_function.valence > 1:
                    graph.remove_node(from_function_name)
        if graph.has_node(to_function_name):
            if to_function.name != to_function_name:
                curr_to_function = ontology.functions[to_function_name]
                if curr_to_function.valence > 1:
                    graph.remove_node(to_function_name)

    if from_function is to_function:
        cycles = [cycle for cycle in nx.simple_cycles(ontology.ontology_graph) if from_function.name in cycle]
        if len(cycles) == 0:
            return 0
        else:
            return min(cycles, key=lambda cycle: len(cycle))

    if not nx.has_path(ontology.ontology_graph, from_function.name, to_function.name):
        path = None
        pathlen = np.inf
    else:
        path = nx.shortest_path(ontology.ontology_graph, from_function.name, to_function.name)
        pathlen = len(path)-1

        assert pathlen > 0

    return 1.0/pathlen



