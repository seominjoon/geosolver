from geosolver.text.lexer.states import Token
import networkx as nx
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

    neutralized_graph = nx.Graph(graph)
    path = nx.shortest_path(neutralized_graph, from_token.index, to_token.index)
    return 1.0/(len(path)-1)


