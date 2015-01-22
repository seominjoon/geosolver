from geosolver.geowordnet import geowordnet
from geosolver.geowordnet.entry_proximity_score import entry_proximity_score
from geosolver.geowordnet.new_function_identifier import new_function_identifier
from geosolver.ontology import basic_ontology, ontology_semantics
from geosolver.ontology.ontology_proximity_score import ontology_proximity_score
from geosolver.text.lexer.string_to_tokens import string_to_tokens
from geosolver.text.semantics.create_semantic_forest import create_semantic_forest
from geosolver.text.semantics.semantic_proximity_score import semantic_proximity_score
from geosolver.text.semantics.shortcuts import create_semantic_nodes
from geosolver.text.syntax.create_syntax import create_syntax
from geosolver.text.syntax.syntax_proximity_score import syntax_proximity_score

__author__ = 'minjoon'

def test_create_semantic_forest():
    string = "Line AB is perpendicular to line CD."
    tokens = string_to_tokens(string)
    syntax = create_syntax(tokens, 3)

    threshold = 0.7
    semantic_nodes = create_semantic_nodes(syntax, basic_ontology, ontology_semantics, geowordnet,
                                           entry_proximity_score, new_function_identifier, tokens, threshold)
    semantic_forest = create_semantic_forest(semantic_nodes,
                                             syntax_proximity_score, ontology_proximity_score, semantic_proximity_score)
    semantic_forest.display_graph()


if __name__ == "__main__":
    test_create_semantic_forest()
