from pprint import pprint
from geosolver.geowordnet import geowordnet
from geosolver.ontology import ontology_semantics, basic_ontology
from geosolver.text.grounding.get_grounded_syntax import get_grounded_syntax
from geosolver.text.grounding.get_grounded_syntax_paths import get_grounded_syntax_paths
from geosolver.text.grounding.get_grounded_tokens import get_grounded_tokens
from geosolver.text.lexer.string_to_tokens import string_to_tokens
from geosolver.text.syntax.create_syntax import create_syntax

__author__ = 'minjoon'


def test_get_grounded_syntax_paths():
    string = "Circle O has a radius of 5."
    tokens = string_to_tokens(string)
    syntax = create_syntax(tokens, 1)
    grounded_tokens = get_grounded_tokens(syntax, ontology_semantics, geowordnet, 0.99)
    pprint(grounded_tokens)

    grounded_syntax = get_grounded_syntax(syntax, basic_ontology, grounded_tokens)
    circle = grounded_syntax.grounded_tokens[(0, 'circle')]
    radius = grounded_syntax.grounded_tokens[(4, 'radiusOf')]
    grounded_syntax_paths = get_grounded_syntax_paths(grounded_syntax, circle, radius)
    pprint(grounded_syntax_paths)

    grounded_syntax.display_graphs()


if __name__ == "__main__":
    test_get_grounded_syntax_paths()