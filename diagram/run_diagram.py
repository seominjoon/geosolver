from geosolver.database.geoserver_interface import geoserver_interface
from geosolver.diagram.parse_diagram import parse_diagram
from geosolver.diagram.parse_image_segments import parse_image_segments
from geosolver.diagram.parse_primitives import parse_primitives, _distance_between_rho_theta_pair_and_point
from geosolver.diagram.select_primitives import select_primitives
from geosolver.ontology.instantiator_definitions import instantiators
from geosolver.utils import open_image
import numpy as np

__author__ = 'minjoon'

def test_parse_image_segments():
    question = geoserver_interface.download_questions(1).values()[0]
    image_segment_parse = parse_image_segments(open_image(question.diagram_path))
    image_segment_parse.display_diagram()
    image_segment_parse.display_labels()


def test_parse_primitives():
    question = geoserver_interface.download_questions(4).values()[0]
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

if __name__ == "__main__":
    # test_parse_image_segments()
    # test_parse_primitives()
    # test_distance_between_rho_theta_pair_and_point()
    # test_select_primitives()
    test_parse_diagram()
