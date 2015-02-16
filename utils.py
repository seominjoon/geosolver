"""
Contains general purpose util functions.
Ideally, this will be made into a separate package later.
"""
import os
import cv2
import networkx as nx
import tempfile
import numpy as np
from PIL import Image

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


def display_graphs(graphs, method='image', block=True):
    for graph in graphs:
        display_graph(graph, method=method, block=False)
    if block:
        block_display()


def block_display():
    cv2.waitKey()
    cv2.destroyAllWindows()


def open_image(filepath, grayscale=True):
    basepath, ext = os.path.splitext(filepath)
    if ext != ".png":
        newpath = basepath + ".png"
        fp = Image.open(filepath)
        fp.save(newpath)
        filepath = newpath
    if grayscale:
        image = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
    else:
        image = cv2.imread(filepath, cv2.IMREAD_COLOR)
    return image

def open_image_from_file(file, grayscale=True):
    fp = Image.open(file)
    _, path = tempfile.mkstemp(suffix=".png")
    fp.save(path)
    if grayscale:
        image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    else:
        image = cv2.imread(path, cv2.IMREAD_COLOR)
    return image


def save_image(image, ext=".png"):
    fp, filepath = tempfile.mkstemp(suffix=ext)
    cv2.imwrite(filepath, image)
    return fp, filepath


def display_image(image, title="", block=True):
    cv2.imshow(title, image)
    if block:
        block_display()


def round_vector(vector):
    return tuple(int(round(x)) for x in vector)


def dimension_wise_non_maximum_suppression(vectors, radii, dimension_wise_distances):
    """
    Performs dimension-wise non maximum suppression.
    vectors is a list of n-dimensional vectors (lists), and
    radii is an n-dimensional vector indicating the radius for each dimension.
    dimension_wise_distances is a function returning distance vector between two vectors.
    Ex. Euclidean dimension-wise distance between (1,2) and (4,1) is (3,1).

    :param vectors:
    :param radii:
    :return:
    """
    out_vectors = []
    if len(vectors) == 0:
        return out_vectors
    assert len(vectors[0]) == len(radii)

    for vector in vectors:
        cond = True
        for vector2 in out_vectors:
            distance_vector = dimension_wise_distances(vector, vector2)
            if all(x <= radii[i] for i, x in enumerate(distance_vector)):
                cond = False
                break

        if cond:
            out_vectors.append(vector)

    return out_vectors


def get_number_string(n, w):
    return ("{0:0%d}" % w).format(n)