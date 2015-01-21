"""
Contains general purpose util functions.
Ideally, this will be made into a separate package later.
"""
import cv2
import networkx as nx
import tempfile

__author__ = 'minjoon'


def save_graph_image(graph, path):
    pydot_graph = nx.to_pydot(graph)
    pydot_graph.write_png(path)


def get_graph_image(graph):
    """
    Returns an image of graph.
    Currently not optimized, as it saves to a temp directory then loads it again.
    If direct conversion to image is found for pydot_graph, please implement it instead.

    :param nx.Graph graph:
    :return np.ndarray:
    """
    _, path = tempfile.mkstemp()
    save_graph_image(graph, path)
    image = cv2.imread(path)
    return image


def display_graph(graph, method='image', title="", block=True):
    """
    Display the graph on the screen.
    Method can be 'image' or 'pyplot'.
    'image' method uses cv2 to display the image file.
    'pyplot' method uses matplotlib to draw the graph on pyplot (not implemented yet).

    :param graph:
    :param method:
    :return:
    """
    if method == 'image':
        image = get_graph_image(graph)
        cv2.imshow(title, image)
        if block:
            block_display()


def block_display():
    cv2.waitKey()
    cv2.destroyAllWindows()