import itertools
import networkx as nx
from geosolver.text.token_grounding.get_grounded_syntax_edge_cost import get_grounded_syntax_edge_cost
from geosolver.text.token_grounding.states import GroundedSyntaxTree
from geosolver.text.syntax.states import SyntaxTree

__author__ = 'minjoon'

def get_grounded_syntax_tree(all_tokens, syntax_tree):
    assert isinstance(syntax_tree, SyntaxTree)

    grounded_graph = nx.DiGraph()

    for grounded_token in all_tokens.values():
        grounded_graph.add_node(grounded_token.key, label=grounded_token.label)

    for u, v, data in syntax_tree.graph.edges(data=True):
        from_grounded_tokens = _filter_tokens(all_tokens, u)
        to_grounded_tokens = _filter_tokens(all_tokens, v)

        for from_, to in itertools.product(from_grounded_tokens.values(), to_grounded_tokens.values()):
            weight = get_grounded_syntax_edge_cost(from_, to, data)
            assert 'weight' not in data
            grounded_graph.add_edge(from_.key, to.key, weight=weight, **data)

    grounded_syntax_tree = GroundedSyntaxTree(all_tokens, grounded_graph, syntax_tree.rank, syntax_tree.score)
    return grounded_syntax_tree

def _filter_tokens(tokens, token_index):
    return {token.key: token for token in tokens.values()
            if token.index == token_index}