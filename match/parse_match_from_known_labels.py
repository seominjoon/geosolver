import networkx as nx

__author__ = 'minjoon'


def parse_match_from_known_labels(general_graph_parse, known_labels):
    """

    :param general_graph_parse:
    :param known_labels: [{'x':96, 'y':110, 'label': 'O', 'type': 'point'}, ]
    :return:
    """
    label_strings = set()
    formulas = {}
    graph = nx.Graph()
    for d in known_labels:
        x = d['x']
        y = d['y']
        label = d['label']
        type_ = d['type']
        arr = type_.split(' ')
        if len(arr > 1):
            type_ = arr[-1]

        # Find closest type_ instance's key in graph_parse

        # Then use the key to get general instance in general graph

        # Wrap the general instance in formula. If there are extra prefixes, add these as well the formula

        # add edge between label and formula