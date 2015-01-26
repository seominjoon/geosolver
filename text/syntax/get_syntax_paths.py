import networkx as nx
from geosolver.text.lexer.states import Token
import numpy as np
from geosolver.text.syntax.states import SyntaxPath

__author__ = 'minjoon'


def get_syntax_paths(syntax, from_token, to_token):
    """

    :param nx.DiGraph graph:
    :param Token from_token:
    :param Token to_token:
    :return dict:
    """
    assert isinstance(from_token, Token)
    assert isinstance(to_token, Token)
    paths = {}
    for idx, syntax_tree in syntax.syntax_trees.iteritems():
        neutralized_graph = nx.Graph(syntax_tree.graph)
        if from_token == to_token:
            cycles = [cycle for cycle in nx.simple_cycles(syntax_tree.graph) if from_token.index in cycle]
            if len(cycles) == 0:
                return paths
            else:
                path = min(cycles, key=lambda cycle: len(cycle))
        else:
            if not nx.has_path(neutralized_graph, from_token.index, to_token.index):
                continue
            path = nx.shortest_path(neutralized_graph, from_token.index, to_token.index)
        token_path = [syntax.tokens[token_idx] for token_idx in path]
        syntax_path = SyntaxPath(syntax, idx, token_path)
        paths[idx] = syntax_path

    return paths

