from geosolver.ontology.states import Formula, OntologyPath

__author__ = 'minjoon'

def tree_graph_to_formula(semantic_forest, tree_graph, head_key):
    """

    :param semantic_forest:
    :param head_type:
    :param tree_graph:
    :return:
    """
    edges = tree_graph.edges(head_key, data=True)
    assert len(edges) == 1
    u, v, data = edges[0]
    formula = _tree_graph_to_formula(semantic_forest, tree_graph, v)
    return formula


def _tree_graph_to_formula(semantic_forest, tree_graph, node_key):
    basic_ontology = semantic_forest.basic_ontology
    function = semantic_forest.all_nodes[node_key]
    children = range(function.valence)
    for u, v, edge_key in tree_graph.edges(node_key, keys=True):
        data = semantic_forest.forest_graph[u][v][edge_key]
        arg_idx = data['arg_idx']
        ontology_path = data['ontology_path']
        v_formula = _tree_graph_to_formula(semantic_forest, tree_graph, v)
        path_formula = _helper(semantic_forest, ontology_path, v_formula)
        children[arg_idx] = path_formula
    formula = Formula(basic_ontology, function, children)
    return formula


def _helper(semantic_forest, ontology_path, v_formula):
    assert isinstance(ontology_path, OntologyPath)
    return _helper2(semantic_forest, ontology_path.path_nodes, v_formula)


def _helper2(semantic_forest, path_nodes, v_formula):
    if len(path_nodes) == 2:
        return v_formula
    else:
        function = path_nodes[1]
        new_path_nodes = path_nodes[1:]
        children = [_helper2(semantic_forest, new_path_nodes, v_formula)]
        return Formula(function, children)