from geosolver.database.geoserver_interface import geoserver_interface
from geosolver.diagram.parse_diagram import parse_diagram
from geosolver.diagram.parse_general_diagram import parse_general_diagram
from geosolver.diagram.parse_general_graph import parse_general_graph
from geosolver.diagram.parse_graph import parse_graph
from geosolver.diagram.parse_image_segments import parse_image_segments
from geosolver.diagram.parse_primitives import parse_primitives
from geosolver.diagram.select_primitives import select_primitives
from geosolver.geowordnet import geowordnet
from geosolver.grounding.ground_semantic_tree import ground_semantic_tree
from geosolver.grounding.parse_match_from_known_labels import parse_match_from_known_labels
from geosolver.grounding.states import GroundedSemanticTree
from geosolver.ontology import ontology_semantics
from geosolver.text.lexer.separate_expressions import separate_expressions
from geosolver.text.lexer.string_to_tokens import string_to_tokens, sentence_to_tokens
from geosolver.text.lexer.string_to_words import string_to_words
from geosolver.text.lexer.words_to_sentences import words_to_sentences
from geosolver.text.semantics.get_semantic_forest import get_semantic_forest
from geosolver.text.semantics.get_semantic_trees import get_semantic_trees
from geosolver.text.syntax.create_syntax import create_syntax
from geosolver.text.token_grounding.get_grounded_syntax import get_grounded_syntax
from geosolver.utils import open_image

__author__ = 'minjoon'

def test_ground_semantic_tree():
    questions = geoserver_interface.download_questions([1])
    for pk, question in questions.iteritems():
        label_data = geoserver_interface.download_labels(pk)[pk]
        image_segment_parse = parse_image_segments(open_image(question.diagram_path))
        primitive_parse = parse_primitives(image_segment_parse)
        selected_primitive_parse = select_primitives(primitive_parse)
        selected_primitive_parse.display_primitives()
        diagram_parse = parse_diagram(selected_primitive_parse)
        print("Parsing graph...")
        graph_parse = parse_graph(diagram_parse)
        print("Graph parsing done.")
        general_diagram_parse = parse_general_diagram(diagram_parse)
        # print(get_evalf_subs(general_diagram_parse.variables, values))
        general_graph_parse = parse_general_graph(general_diagram_parse, graph_parse)
        match_parse = parse_match_from_known_labels(general_graph_parse, label_data)
        # print(match_parse.match_graph['A']['B'])


        # Text processing
        threshold = 0.99
        sentences = words_to_sentences(string_to_words(question.text))
        for sentence in sentences:
            tokens, equations = separate_expressions(sentence)
            print(tokens)
            syntax = create_syntax(tokens, 1)
            grounded_syntax = get_grounded_syntax(syntax, ontology_semantics, geowordnet, threshold)
            truth = grounded_syntax.basic_ontology.types['truth']
            semantic_forest = get_semantic_forest(grounded_syntax, 3, 3)
            semantic_trees = get_semantic_trees(semantic_forest, truth)
            for semantic_tree in semantic_trees.values():
                print(semantic_tree.formula)
                grounded_semantic_trees = ground_semantic_tree(match_parse, semantic_tree)
                for grounded_semantic_tree in grounded_semantic_trees:
                    assert isinstance(grounded_semantic_tree, GroundedSemanticTree)
                    print(grounded_semantic_tree.grounded_formula)


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
    test_ground_semantic_tree()
