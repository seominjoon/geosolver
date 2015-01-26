"""
Non-important (usually for debugging) methods
"""
from geosolver.utils import display_graph, block_display

__author__ = 'minjoon'


def syntax_display_graphs(syntax):
    for syntax_tree in syntax.syntax_trees.values():
        display_graph(syntax_tree.graph, title="%f" % syntax_tree.score, block=False)
    block_display()

