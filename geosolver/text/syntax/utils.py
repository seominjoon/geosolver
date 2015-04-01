import networkx as nx
__author__ = 'minjoon'


def match_trees(tree0, tree1, match_edge_label=False):
    """
    Returns True if tree0 and tree1 are identical.
    Edge labels are not considered unless match_edge_label is set to True.

    :param tree0:
    :param tree1:
    :param match_edge_label:
    :return:
    """
    assert isinstance(tree0, nx.DiGraph)
    assert isinstance(tree1, nx.DiGraph)
    for u, v, data in tree0.edges(data=True):
        if not tree1.has_edge(u, v):
            return False
        if match_edge_label and data['label'] != tree1[u][v]['label']:
            return False
    return True
