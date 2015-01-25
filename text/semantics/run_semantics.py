from geosolver.geowordnet import geowordnet
from geosolver.ontology import basic_ontology, ontology_semantics
from geosolver.text.lexer.string_to_tokens import string_to_tokens
from geosolver.text.semantics.create_semantic_forest import create_semantic_forest
from geosolver.text.semantics.create_semantic_nodes import create_semantic_nodes
from geosolver.text.syntax.create_syntax import create_syntax

__author__ = 'minjoon'

def test_create_semantic_forest():
    string = "Circle O has a radius of 5."
    tokens = string_to_tokens(string)
    syntax = create_syntax(tokens, 3)

    threshold = 0.99
    semantic_nodes = create_semantic_nodes(syntax, basic_ontology, ontology_semantics, geowordnet, tokens, threshold)
    semantic_forest = create_semantic_forest(semantic_nodes, 3.0, 1.0)
    semantic_forest.display_graph()


if __name__ == "__main__":
    test_create_semantic_forest()
