import networkx as nx
from geosolver.text.lexer.states import Token

__author__ = 'minjoon'

def syntax_proximity_score(syntax, from_token, to_token):
    """
    Given syntax (i.e. a set of graphs), measure distance between from_token to to_token.
    For now, use minimum of distance between from_token and to_token in all dependency trees.

    :param syntax:
    :param from_token:
    :param to_token:
    :return:
    """
    return min(_graph_proximity_score(graph, from_token, to_token) for graph, score in syntax.syntax_graph_score_pairs)


def _graph_proximity_score(graph, from_token, to_token):
    """

    :param nx.DiGraph graph:
    :param Token from_token:
    :param Token to_token:
    :return float:
    """
    assert isinstance(from_token, Token)
    assert isinstance(to_token, Token)

    if from_token is to_token:
        cycles = [cycle for cycle in nx.simple_cycles(graph) if from_token.index in cycle]
        if len(cycles) == 0:
            return 0
        else:
            return min(cycles, key=lambda cycle: len(cycle))

    neutralized_graph = nx.Graph(graph)
    path = nx.shortest_path(neutralized_graph, from_token.index, to_token.index)
    pathlen = len(path) - 1
    assert pathlen > 0
    return 1.0/pathlen


