import itertools
import networkx as nx
from geosolver.text.grounding.states import GroundedSyntaxTree
from geosolver.text.syntax.states import SyntaxTree

__author__ = 'minjoon'

def get_grounded_syntax_tree(grounded_tokens, syntax_tree):
    assert isinstance(syntax_tree, SyntaxTree)

    grounded_graph = nx.DiGraph()

    for grounded_token in grounded_tokens.values():
        grounded_graph.add_node(grounded_token.key, label=grounded_token.label)

    for u, v, data in syntax_tree.graph.edges(data=True):

        from_grounded_tokens = _filter_grounded_tokens(grounded_tokens, u)
        to_grounded_tokens = _filter_grounded_tokens(grounded_tokens, v)

        for from_, to in itertools.product(from_grounded_tokens.values(), to_grounded_tokens.values()):
            grounded_graph.add_edge(from_.key, to.key, **data)

    grounded_syntax_tree = GroundedSyntaxTree(grounded_tokens, grounded_graph, syntax_tree.rank, syntax_tree.score)
    return grounded_syntax_tree

def _filter_grounded_tokens(grounded_tokens, token_index):
    return {grounded_token.key: grounded_token for grounded_token in grounded_tokens.values()
            if grounded_token.index == token_index}