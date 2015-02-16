from pprint import pprint
from geosolver.geowordnet import geowordnet
from geosolver.ontology import basic_ontology, ontology_semantics
from geosolver.text.semantics.costs.get_semantic_tree_cost import get_semantic_tree_cost
from geosolver.text.semantics.get_semantic_trees import get_semantic_trees
from geosolver.text.token_grounding.get_grounded_syntax import get_grounded_syntax
from geosolver.text.token_grounding.get_grounded_tokens import get_grounded_tokens
from geosolver.text.lexer.string_to_tokens import string_to_tokens
from geosolver.text.semantics.get_semantic_forest import get_semantic_forest
from geosolver.text.syntax.create_syntax import create_syntax

__author__ = 'minjoon'

def test_get_semantic_trees():
    string = "Circle O has a radius of 5."
    tokens = string_to_tokens(string)
    print("Tokens initalized.")
    syntax = create_syntax(tokens, 10)
    syntax.display_graphs()
    print("Syntax initialized.")
    threshold = 0.99
    grounded_syntax = get_grounded_syntax(syntax, ontology_semantics, geowordnet, threshold)
    print("Grounded syntax initialized.")
    semantic_forest = get_semantic_forest(grounded_syntax, 3, 3)
    print("Forest initialized.")
    truth = grounded_syntax.basic_ontology.types['truth']
    qnumber = grounded_syntax.basic_ontology.types['uNumber']
    semantic_trees = get_semantic_trees(semantic_forest, truth)

    grounded_syntax.display_graphs()
    semantic_forest.display_graph()
    print(len(semantic_trees))
    for semantic_tree in semantic_trees.values():
        print(get_semantic_tree_cost(semantic_tree))
        print(semantic_tree.formula)
        semantic_tree.display_graph()

if __name__ == "__main__":
    test_get_semantic_trees()
