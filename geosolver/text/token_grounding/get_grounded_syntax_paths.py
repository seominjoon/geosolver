from geosolver.text.token_grounding.states import GroundedSyntaxPath
from geosolver.text.lexer.states import Token
import networkx as nx

__author__ = 'minjoon'

def get_grounded_syntax_paths(grounded_syntax, from_token, to_token):
    """

    :param grounded_syntax:
    :param from_token:
    :param to_token:
    :return dict:
    """
    assert isinstance(from_token, Token)
    assert isinstance(to_token, Token)
    all_token_paths = {}
    for rank, grounded_syntax_tree in grounded_syntax.grounded_syntax_trees.iteritems():
        paths = []
        neutralized_graph = nx.Graph(grounded_syntax_tree.graph)
        if from_token == to_token:
            continue
        else:
            if not nx.has_path(neutralized_graph, from_token.key, to_token.key):
                continue
            path = nx.shortest_path(neutralized_graph, from_token.key, to_token.key, weight='weight')
            cost = nx.shortest_path_length(neutralized_graph, from_token.key, to_token.key, weight='weight')
        token_path = _ground_path(grounded_syntax, path)
        syntax_path = GroundedSyntaxPath(grounded_syntax, rank, token_path, cost)
        all_token_paths[rank] = syntax_path

    return all_token_paths


def _ground_path(grounded_syntax, path):
    return [grounded_syntax.all_tokens[key] for key in path]
