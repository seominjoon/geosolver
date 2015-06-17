"""
Matching is aligning labels and objects in diagram given entity formulas.
This package also provides mapping from text formula to diagram formula.


at the end, we just want string mapping to formula (one can maps to multiple,
so use graph)

"""

__author__ = 'minjoon'


class MatchNetwork(object):
    pass


class MatchParse(object):
    def __init__(self, general_graph_parse, label_strings, formulas, match_graph):
        """
        graph encodes mapping from label_strings to formulas.
        Everything is formula. Even entity itself is a formula.

        :param GraphParse graph_parse:
        :param set label_strings:
        :param dict formulas: contains formulas
        :param nx.Graph graph:
        :return:
        """
        self.general_graph_parse = general_graph_parse
        self.label_strings = label_strings
        self.formulas = formulas
        self.match_graph = match_graph

class GroundedSemanticTree(object):
    def __init__(self, semantic_tree, grounded_formula, cost, variables):
        self.semantic_tree = semantic_tree
        self.grounded_formula = grounded_formula
        self.cost = cost
        self.variables = variables

class Temp(object):
    def __init__(self, graph_parse, known_labels, match_dict):
        self.graph_parse = graph_parse
        self.known_labels = known_labels
        self.match_dict = match_dict
