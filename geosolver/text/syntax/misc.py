"""
Non-important (usually for debugging) methods
"""
import os

from geosolver.utils.prep import display_graph, block_display, save_graph_image, get_number_string

__author__ = 'minjoon'


def syntax_display_graphs(syntax):
    for syntax_tree in syntax.syntax_trees.values():
        display_graph(syntax_tree.graph, title="%f" % syntax_tree.score, block=False)
    block_display()


def syntax_save_graphs(syntax, root_path):
    for idx, syntax_tree in syntax.syntax_trees.iteritems():
        file_name = "%s.png" % get_number_string(idx, 2)
        full_path = os.path.join(root_path, file_name)
        save_graph_image(syntax_tree.graph, full_path)

