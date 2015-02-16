from pprint import pprint

from geosolver.geowordnet import geowordnet
from geosolver.ontology import ontology_semantics
from geosolver.ontology.get_ontology_paths import get_ontology_paths
from geosolver.text.token_grounding.get_grounded_syntax import get_grounded_syntax
from geosolver.text.token_grounding.get_grounded_syntax_paths import get_grounded_syntax_paths
from geosolver.text.lexer.string_to_tokens import string_to_tokens
from geosolver.text.semantics.costs.get_grounded_syntax_path_cost import get_grounded_syntax_path_cost
from geosolver.text.semantics.costs.get_ontology_path_cost import get_ontology_path_cost
from geosolver.text.syntax.create_syntax import create_syntax


__author__ = 'minjoon'


def test_get_grounded_syntax_paths():
    string = "Circle O has a radius of 5."
    tokens = string_to_tokens(string)
    syntax = create_syntax(tokens, 1)
    grounded_syntax = get_grounded_syntax(syntax, ontology_semantics, geowordnet, 0.99)
    circle = grounded_syntax.grounded_tokens[(0, 'circle')]
    radius = grounded_syntax.grounded_tokens[(4, 'radiusOf')]
    grounded_syntax_paths = get_grounded_syntax_paths(grounded_syntax, circle, radius)
    ontology_paths = get_ontology_paths(grounded_syntax.basic_ontology, radius.ground.arg_types[0], circle.ground)
    print(ontology_paths)
    print(get_grounded_syntax_path_cost(grounded_syntax_paths[0]))
    print(get_ontology_path_cost(ontology_paths[0]))
    pprint(grounded_syntax_paths)
    pprint(ontology_paths)

    grounded_syntax.display_graphs()


if __name__ == "__main__":
    test_get_grounded_syntax_paths()