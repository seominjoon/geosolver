from geosolver.text.token_grounding.states import GroundedSyntaxPath, GroundedToken

__author__ = 'minjoon'


def get_grounded_syntax_path_cost(grounded_syntax_path):
    assert isinstance(grounded_syntax_path, GroundedSyntaxPath)
    return grounded_syntax_path.cost
