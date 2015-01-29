from geosolver.ontology.states import Formula, OntologyPath

__author__ = 'minjoon'

def tree_graph_to_formula(semantic_forest, tree_graph, node_key):
    basic_ontology = semantic_forest.basic_ontology
    function = semantic_forest.graph_nodes[node_key].function
    children = range(function.valence)
    from_index = [x for x, data in tree_graph.nodes(data=True) if data['key'] == node_key][0]
    for _, to_index, data in tree_graph.edges(from_index, data=True):
        u = tree_graph.node[from_index]['key']
        v = tree_graph.node[to_index]['key']
        data = semantic_forest.forest_graph[u][v][data['key']]
        arg_idx = data['arg_idx']
        ontology_path = data['ontology_path']
        v_formula = tree_graph_to_formula(semantic_forest, tree_graph, v)
        path_formula = _helper(semantic_forest, ontology_path, v_formula)
        children[arg_idx] = path_formula
    formula = Formula(basic_ontology, function, children)
    return formula


def _helper(semantic_forest, ontology_path, v_formula):
    assert isinstance(ontology_path, OntologyPath)
    return _helper2(semantic_forest, ontology_path.path_nodes, v_formula)


def _helper2(semantic_forest, path_nodes, v_formula):
    if len(path_nodes) == 3:
        return v_formula
    else:
        basic_ontology = semantic_forest.basic_ontology
        function = path_nodes[2]
        new_path_nodes = path_nodes[2:]
        children = [_helper2(semantic_forest, new_path_nodes, v_formula)]
        return Formula(basic_ontology, function, children)