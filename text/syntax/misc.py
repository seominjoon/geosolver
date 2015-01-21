"""
Non-important (usually for debugging) methods
"""
from geosolver.utils import display_graph, block_display

__author__ = 'minjoon'


def syntax_display_graphs(syntax):
    for graph, score in syntax.syntax_graph_score_pairs:
        display_graph(graph, title="%f" % score, block=False)
    block_display()

