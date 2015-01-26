from pprint import pprint
from geosolver.geowordnet import geowordnet
from geosolver.ontology import basic_ontology, ontology_semantics
from geosolver.text.token_grounding.get_grounded_syntax import get_grounded_syntax
from geosolver.text.token_grounding.get_grounded_tokens import get_grounded_tokens
from geosolver.text.lexer.string_to_tokens import string_to_tokens
from geosolver.text.semantics.get_semantic_forest import get_semantic_forest
from geosolver.text.syntax.create_syntax import create_syntax

__author__ = 'minjoon'

def test_create_semantic_forest():
    string = "Circle O has a radius of 5."
    tokens = string_to_tokens(string)
    syntax = create_syntax(tokens, 1)
    threshold = 0.99
    grounded_tokens = get_grounded_tokens(syntax, ontology_semantics, geowordnet, threshold)
    grounded_syntax = get_grounded_syntax(grounded_tokens)
    semantic_forest = get_semantic_forest(grounded_syntax, 3, 3)
    semantic_forest.display_graph()


if __name__ == "__main__":
    test_create_semantic_forest()
