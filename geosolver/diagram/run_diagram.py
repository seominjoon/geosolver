import itertools
from geosolver.database.geoserver_interface import geoserver_interface
from geosolver.diagram.get_evalf_subs import get_evalf_subs
from geosolver.diagram.computational_geometry import distance_between_points, cartesian_angle
from geosolver.diagram.get_instances import get_instances, get_all_instances
from geosolver.diagram.instance_exists import instance_exists
from geosolver.diagram.parse_diagram import parse_diagram
from geosolver.diagram.parse_general_diagram import parse_general_diagram
from geosolver.diagram.parse_general_graph import parse_general_graph
from geosolver.diagram.parse_graph import parse_graph
from geosolver.diagram.parse_image_segments import parse_image_segments
from geosolver.diagram.parse_primitives import parse_primitives, _distance_between_rho_theta_pair_and_point
from geosolver.diagram.select_primitives import select_primitives
from geosolver.grounding.label_distances import label_distance_to_angle
from geosolver.grounding.parse_match_from_known_labels import parse_match_from_known_labels
from geosolver.ontology.instantiator_definitions import instantiators
from geosolver.utils import open_image, display_graph
import numpy as np

__author__ = 'minjoon'

def test_parse_image_segments():
    question = geoserver_interface.download_questions(1).values()[0]
    image_segment_parse = parse_image_segments(open_image(question.diagram_path))
    image_segment_parse.display_diagram()
    image_segment_parse.display_labels()


def test_parse_primitives():
    question = geoserver_interface.download_questions([1]).values()[0]
    image_segment_parse = parse_image_segments(open_image(question.diagram_path))
    primitive_parse = parse_primitives(image_segment_parse)
    primitive_parse.display_primitives()


def test_select_primitives():
    questions = geoserver_interface.download_questions().values()
    parses = []
    for question in questions[:80]:
        print(question.key)
        image_segment_parse = parse_image_segments(open_image(question.diagram_path))
        primitive_parse = parse_primitives(image_segment_parse)
        # primitive_parse.display_each_primitive()
        selected = select_primitives(primitive_parse)
        parses.append(selected)

    for parse in parses:
        parse.display_primitives()

def test_parse_diagram():
    questions = geoserver_interface.download_questions().values()
    parses = []
    for question in questions[:10]:
        print(question.key)
        image_segment_parse = parse_image_segments(open_image(question.diagram_path))
        primitive_parse = parse_primitives(image_segment_parse)
        # primitive_parse.display_each_primitive()
        selected = select_primitives(primitive_parse)
        # selected.display_primitives()
        diagram_parse = parse_diagram(selected)
        parses.append(diagram_parse)

    for parse in parses:
        parse.display_points()



def test_distance_between_rho_theta_pair_and_point():
    rho_theta_pair = (1, np.pi/4)
    point = instantiators['point'](-1, -1)
    print(_distance_between_rho_theta_pair_and_point(rho_theta_pair, point))


def test_instance_exists():
    questions = geoserver_interface.download_questions(1).values()
    parses = []
    for question in questions[:10]:
        print(question.key)
        image_segment_parse = parse_image_segments(open_image(question.diagram_path))
        primitive_parse = parse_primitives(image_segment_parse)
        # primitive_parse.display_each_primitive()
        selected = select_primitives(primitive_parse)
        selected.display_primitives()
        diagram_parse = parse_diagram(selected)
        diagram_parse.display_points()

        for p0, p1, p2 in itertools.permutations(diagram_parse.intersection_points.values(), 3):
            radius1 = distance_between_points(p0, p1)
            radius2 = distance_between_points(p0, p2)
            if abs(radius1-radius2)/(radius1+radius2) < 0.1:
                radius = (radius1+radius2)/2.0
                circle = instantiators['circle'](p0, radius)
                arc = instantiators['arc'](circle, p1, p2)
                if instance_exists(diagram_parse, arc):
                    diagram_parse.display_instance(arc)

        parses.append(diagram_parse)


def test_parse_graph():
    questions = geoserver_interface.download_questions([1]).values()
    for question in questions:
        image_segment_parse = parse_image_segments(open_image(question.diagram_path))
        primitive_parse = parse_primitives(image_segment_parse)
        selected_primitive_parse = select_primitives(primitive_parse)
        diagram_parse = parse_diagram(selected_primitive_parse)
        diagram_parse.display_points()
        print("Parsing graph...")
        graph_parse = parse_graph(diagram_parse)
        print("Graph parsing done.")
        general_diagram_parse = parse_general_diagram(diagram_parse)
        print(get_evalf_subs(general_diagram_parse.variables, general_diagram_parse.values))
        general_graph_parse = parse_general_graph(general_diagram_parse, graph_parse)
        lines = get_all_instances(graph_parse, 'line')
        circles = get_all_instances(graph_parse, 'circle')
        arcs = get_all_instances(graph_parse, 'arc')
        angles = get_all_instances(graph_parse, 'angle')
        """
        for angle in angles.values():
            print(angle)
            graph_parse.display_instances([angle])
        """
        for a, b, c in itertools.combinations(graph_parse.diagram_parse.intersection_points, 3):
            triangles = get_instances(graph_parse, 'triangle', a, b, c)
            print(triangles)
            graph_parse.display_instances(triangles.values())


def test_substitute_variables():
    questions = geoserver_interface.download_questions([1]).values()
    for question in questions:
        image_segment_parse = parse_image_segments(open_image(question.diagram_path))
        primitive_parse = parse_primitives(image_segment_parse)
        selected = select_primitives(primitive_parse)
        diagram_parse = parse_diagram(selected)
        general_diagram_parse = parse_general_diagram(diagram_parse)
        print(general_diagram_parse.variables)
        diagram_parse.display_points()



def test_parse_match():
    questions = geoserver_interface.download_questions([2])
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
        for label in match_parse.label_strings:
            formula_keys = match_parse.match_graph[label].keys()
            print(label)
            print([match_parse.formulas[key] for key in formula_keys])
        print(general_diagram_parse.variables)
        diagram_parse.display_points()

def test_temp():
    pa = instantiators['point'](1,2)
    pb = instantiators['point'](0,0)
    pc = instantiators['point'](-2,1)
    pp = instantiators['point'](0,2)
    angle = instantiators['angle'](pa, pb, pc)
    print(label_distance_to_angle(pp, angle))


if __name__ == "__main__":
    # test_parse_image_segments()
    # test_parse_primitives()
    # test_distance_between_rho_theta_pair_and_point()
    # test_select_primitives()
    # test_parse_diagram()
    # test_instance_exists()
    # test_parse_graph()
    # test_parse_match()
    # test_temp()
    test_substitute_variables()
