from geosolver.database.geoserver_interface import geoserver_interface
from geosolver.diagram.shortcuts import diagram_to_graph_parse
from geosolver.grounding.parse_match_from_known_labels import temp
from geosolver.utils import open_image

__author__ = 'minjoon'

def test_parse_match_from_known_labels():
    questions = geoserver_interface.download_questions(['test'])
    for pk, question in questions.iteritems():
        label_data = geoserver_interface.download_labels(pk)[pk]
        diagram = open_image(question.diagram_path)
        graph_parse = diagram_to_graph_parse(diagram)
        match_parse = temp(graph_parse, label_data)
        for key, value in match_parse.match_dict.iteritems():
            print match_parse.known_labels[key]['label'], value
        graph_parse.diagram_parse.display_points()

if __name__ == "__main__":
    test_parse_match_from_known_labels()
