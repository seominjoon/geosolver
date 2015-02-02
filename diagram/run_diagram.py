from geosolver.database.geoserver_interface import geoserver_interface
from geosolver.diagram.parse_image_segments import parse_image_segments
from geosolver.diagram.parse_primitives import parse_primitives
from geosolver.utils import open_image

__author__ = 'minjoon'

def test_parse_image_segments():
    question = geoserver_interface.download_questions(1).values()[0]
    image_segment_parse = parse_image_segments(open_image(question.diagram_path))
    image_segment_parse.display_diagram()
    image_segment_parse.display_labels()


def test_parse_primitives():
    question = geoserver_interface.download_questions(1).values()[0]
    image_segment_parse = parse_image_segments(open_image(question.diagram_path))
    primitive_parse = parse_primitives(image_segment_parse)
    primitive_parse.display_primitives()

if __name__ == "__main__":
    # test_parse_image_segments()
    test_parse_primitives()
