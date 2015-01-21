import networkx as nx
import numpy as np

__author__ = 'minjoon'


def ontology_proximity_score(ontology, from_symbol, to_symbol):
    """
    Given two function_defs, returns the proximity of to_symbol from from_symbol.
    For now, returns the inverse of the shortest distance from from_symbol to to_symbol

    :param geosolver.ontology.states.Ontology ontology:
    :param geosolver.ontology.states.Function from_symbol:
    :param geosolver.ontology.states.Function to_symbol:
    :return float:
    """
    if not nx.has_path(ontology.ontology_graph, from_symbol.name, to_symbol.name):
        path = None
        pathlen = np.inf
    else:
        path = nx.shortest_path(ontology.ontology_graph, from_symbol.name, to_symbol.name)
        pathlen = len(path)-1

    return 1.0/pathlen



