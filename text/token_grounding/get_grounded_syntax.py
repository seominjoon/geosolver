from geosolver.text.token_grounding.get_grounded_syntax_tree import get_grounded_syntax_tree
from geosolver.text.token_grounding.get_grounded_tokens import get_grounded_tokens
from geosolver.text.token_grounding.states import GroundedSyntax

__author__ = 'minjoon'


def get_grounded_syntax(syntax, ontology_semantics, geowordnet, threshold):
    grounded_tokens = get_grounded_tokens(syntax, ontology_semantics, geowordnet, threshold)

    grounded_syntax_trees = {}
    all_tokens = dict(grounded_tokens.items() + syntax.tokens.items())
    for syntax_tree in syntax.syntax_trees.values():
        grounded_syntax_tree = get_grounded_syntax_tree(all_tokens, syntax_tree)
        grounded_syntax_trees[grounded_syntax_tree.rank] = grounded_syntax_tree

    grounded_syntax = GroundedSyntax(syntax, geowordnet.basic_ontology, grounded_tokens, grounded_syntax_trees)
    return grounded_syntax