from geosolver.text.semantics.states import ImpliedInstance
from geosolver.text.syntax.states import SyntaxTree
from geosolver.text.token_grounding.states import GroundedSyntax

__author__ = 'minjoon'


def get_implied_instance_cost(implied_instance):
    grounded_syntax = implied_instance.grounded_syntax
    assert isinstance(grounded_syntax, GroundedSyntax)
    assert isinstance(implied_instance, ImpliedInstance)
    basic_ontology = grounded_syntax.basic_ontology
    if implied_instance.ground.type == basic_ontology.types['reference']:
        for syntax_tree in grounded_syntax.syntax_trees.values():
            assert isinstance(syntax_tree, SyntaxTree)
            for u, v, data in syntax_tree.graph.edges(implied_instance.parent_grounded_token.key):
                child_grounded_token = grounded_syntax.grounded_tokens[v]
                if child_grounded_token.function.return_type == basic_ontology.types['reference']:
                    return 100
                else:
                    return 1
    elif basic_ontology.isinstance(implied_instance.ground.type, basic_ontology.types['entity']):
        return 4

    return 100
