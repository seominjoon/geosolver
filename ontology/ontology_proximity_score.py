import networkx as nx
import numpy as np

__author__ = 'minjoon'


def ontology_proximity_score(ontology, from_function, to_function):
    """
    Given two function_defs, returns the proximity of to_function from from_function.
    For now, returns the inverse of the shortest distance from from_function to to_function
    If from_function and to_function are the same,
    then for the score to be non-zero, there has to exist a cycle.

    :param geosolver.basic_ontology.states.Ontology basic_ontology:
    :param geosolver.basic_ontology.states.Function from_function:
    :param geosolver.basic_ontology.states.Function to_function:
    :return float:
    """
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



