import itertools
from geosolver.text.semantics.costs.get_grounded_syntax_path_cost import get_grounded_syntax_path_cost
from geosolver.text.token_grounding.get_grounded_syntax_paths import get_grounded_syntax_paths

__author__ = 'minjoon'


def get_implied_parent_function_cost(implied_parent_function):
    """
    Sum of syntax costs between all combinations of children.

    :param implied_parent_function:
    :return float:
    """
    grounded_syntax = implied_parent_function.grounded_syntax
    grounded_tokens = grounded_syntax.grounded_tokens
    cost_sum = 0
    for gt0, gt1 in itertools.combinations(grounded_tokens.values(), 2):
        if gt0.index == gt1.index:
            continue
        grounded_syntax_paths = get_grounded_syntax_paths(grounded_syntax, gt0, gt1)
        cost = min(get_grounded_syntax_path_cost(grounded_syntax_path)
                   for grounded_syntax_path in grounded_syntax_paths.values())
        cost_sum += cost

    return cost_sum
