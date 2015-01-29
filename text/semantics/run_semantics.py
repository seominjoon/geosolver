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

def test_create_semantic_forest():
    string = "Given: tangent AD, diameter CD, secant AC in circle O shown at the right."
    tokens = string_to_tokens(string)
    print("Tokens initalized.")
    syntax = create_syntax(tokens, 1)
    print("Syntax initialized.")
    threshold = 0.99
    grounded_tokens = get_grounded_tokens(syntax, ontology_semantics, geowordnet, threshold)
    print("Groudned tokens initialized.")
    if len(grounded_tokens) == 0:
        raise Exception()
    grounded_syntax = get_grounded_syntax(grounded_tokens)
    print("Grounded syntax initialized.")
    semantic_forest = get_semantic_forest(grounded_syntax, 8, 4)
    print("Forest initialized.")
    truth = grounded_syntax.basic_ontology.types['truth']
    qnumber = grounded_syntax.basic_ontology.types['?number']
    semantic_trees = get_semantic_trees(semantic_forest, truth)

    # grounded_syntax.display_graphs()
    # semantic_forest.display_graph()
    print(len(semantic_trees))
    for semantic_tree in semantic_trees.values():
        print(get_semantic_tree_cost(semantic_tree))
        print(semantic_tree.formula)
        semantic_tree.display_graph()

if __name__ == "__main__":
    test_create_semantic_forest()
