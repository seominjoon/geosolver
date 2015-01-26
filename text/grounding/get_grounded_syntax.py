from geosolver.text.grounding.get_grounded_syntax_tree import get_grounded_syntax_tree
from geosolver.text.grounding.states import GroundedSyntax

__author__ = 'minjoon'


def get_grounded_syntax(syntax, basic_ontology, grounded_tokens):
    grounded_syntax_trees = {}
    for syntax_tree in syntax.syntax_trees.values():
        grounded_syntax_tree = get_grounded_syntax_tree(grounded_tokens, syntax_tree)
        grounded_syntax_trees[grounded_syntax_tree.rank] = grounded_syntax_tree

    grounded_syntax = GroundedSyntax(syntax, basic_ontology, grounded_tokens, grounded_syntax_trees)
    return grounded_syntax