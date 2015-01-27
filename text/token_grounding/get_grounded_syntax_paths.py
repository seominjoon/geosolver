from geosolver.text.token_grounding.states import GroundedSyntaxPath
from geosolver.text.lexer.states import Token
import networkx as nx

__author__ = 'minjoon'

def get_grounded_syntax_paths(grounded_syntax, from_token, to_token):
    assert isinstance(from_token, Token)
    assert isinstance(to_token, Token)
    all_token_paths = {}
    for rank, grounded_syntax_tree in grounded_syntax.grounded_syntax_trees.iteritems():
        paths = []
        neutralized_graph = nx.Graph(grounded_syntax_tree.graph)
        if from_token == to_token:
            cycles = [cycle for cycle in nx.simple_cycles(grounded_syntax_tree.graph)
                      if from_token.key in cycle]
            for cycle in cycles:
                paths.append(cycle)
        else:
            if not nx.has_path(neutralized_graph, from_token.key, to_token.key):
                continue
            paths = nx.all_simple_paths(neutralized_graph, from_token.key, to_token.key)
        token_paths = [_ground_path(grounded_syntax, path) for path in paths]
        syntax_paths = [GroundedSyntaxPath(grounded_syntax, rank, token_path) for token_path in token_paths]
        for idx, syntax_path in enumerate(syntax_paths):
            all_token_paths[(rank, idx)] = syntax_path

    return all_token_paths


def _ground_path(grounded_syntax, path):
    return [grounded_syntax.all_tokens[key] for key in path]
