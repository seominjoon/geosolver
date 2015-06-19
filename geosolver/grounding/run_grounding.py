from geosolver import geoserver_interface
from geosolver.diagram.shortcuts import diagram_to_graph_parse
from geosolver.grounding.ground_atoms import ground_atoms
from geosolver.grounding.parse_match_atoms import parse_match_atoms
from geosolver.grounding.parse_match_from_known_labels import parse_match_from_known_labels
from geosolver.text2.ontology import FunctionNode, function_signatures, VariableSignature
from geosolver.utils import open_image

__author__ = 'minjoon'

def test_parse_match_from_known_labels():
    questions = geoserver_interface.download_questions(977)
    for pk, question in questions.iteritems():
        label_data = geoserver_interface.download_labels(pk)[pk]
        diagram = open_image(question.diagram_path)
        graph_parse = diagram_to_graph_parse(diagram)
        match_parse = parse_match_from_known_labels(graph_parse, label_data)
        for key, value in match_parse.match_dict.iteritems():
            print key, value
        graph_parse.core_parse.display_points()


def test_parse_match_atoms():
    questions = geoserver_interface.download_questions(977)
    for pk, question in questions.iteritems():
        label_data = geoserver_interface.download_labels(pk)[pk]
        diagram = open_image(question.diagram_path)
        graph_parse = diagram_to_graph_parse(diagram)
        match_parse = parse_match_from_known_labels(graph_parse, label_data)
        match_atoms = parse_match_atoms(match_parse)
        for match_atom in match_atoms:
            print match_atom
        graph_parse.core_parse.display_points()

def f(name, *args):
    return FunctionNode(function_signatures[name], args)
def v(name, return_type):
    vs = VariableSignature(name, return_type)
    return FunctionNode(vs, [])

def test_ground_atoms():
    pk = 973
    questions = geoserver_interface.download_questions(pk)
    question = questions.values()[0]

    label_data = geoserver_interface.download_labels(pk)[pk]
    diagram = open_image(question.diagram_path)
    graph_parse = diagram_to_graph_parse(diagram)
    match_parse = parse_match_from_known_labels(graph_parse, label_data)


    AB = v('AB', 'line')
    AC = v('AC', 'line')
    BC = v('BC', 'line')
    ED = v('ED', 'line')
    AE = v('AE', 'line')
    E = v('E', 'point')
    D = v('D', 'point')
    x = v('x', 'number')
    p1 = f('LengthOf', AB) == f('LengthOf', AC)
    p4 = f('LengthOf', AE) == x
    p5 = f('LengthOf', ED) == 4

    grounded_atoms = ground_atoms(match_parse, [p1, p4, p5])
    for grounded_atom in grounded_atoms:
        print grounded_atom

    graph_parse.core_parse.display_points()


if __name__ == "__main__":
    # test_parse_match_from_known_labels()
    test_ground_atoms()
