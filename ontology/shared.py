"""
Shared functions to be included in states.py for convenience.
To avoid cyclic dependencies among modules.
Won't be accessed directly by modules outside of this package, in general.
"""
import networkx as nx

__author__ = 'minjoon'


def isinstance_(inheritance_graph, type0, type1):
    """
    Returns True if type0 is an instance of type1;
    i.e. if type1 is reachable by type0 in inheritance graph.

    :param nx.DiGraph inheritance_graph:
    :param geosolver.basic_ontology.states.Type type0:
    :param geosolver.basic_ontology.states.Type type1:
    :return bool:
    """
    return nx.has_path(inheritance_graph, type1.name, type0.name)


