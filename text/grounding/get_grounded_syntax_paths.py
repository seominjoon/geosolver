from geosolver.text.grounding.states import GroundedSyntaxPath
from geosolver.text.lexer.states import Token
import networkx as nx

__author__ = 'minjoon'

def get_grounded_syntax_paths(grounded_syntax, from_token, to_token):
    assert isinstance(from_token, Token)
    assert isinstance(to_token, Token)
    paths = {}
    for rank, grounded_syntax_tree in grounded_syntax.grounded_syntax_trees.iteritems():
        neutralized_graph = nx.Graph(grounded_syntax_tree.graph)
        if from_token == to_token:
            cycles = [cycle for cycle in nx.simple_cycles(grounded_syntax_tree.grounded_graph)
                      if from_token.key in cycle]
            if len(cycles) == 0:
                return paths
            else:
                path = min(cycles, key=lambda c: len(c))
        else:
            if not nx.has_path(neutralized_graph, from_token.key, to_token.key):
                continue
            path = nx.shortest_path(neutralized_graph, from_token.key, to_token.key)
        token_path = [grounded_syntax.grounded_tokens[key] for key in path]
        syntax_path = GroundedSyntaxPath(grounded_syntax, rank, token_path)
        paths[rank] = syntax_path

    return paths
