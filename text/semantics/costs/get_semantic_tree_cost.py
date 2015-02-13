from geosolver.text.semantics.states import SemanticTree
from geosolver.text.token_grounding.states import GroundedToken

__author__ = 'minjoon'

def get_semantic_tree_cost(semantic_tree):
    semantic_forest = semantic_tree.semantic_forest
    basic_ontology = semantic_tree.basic_ontology
    reference = basic_ontology.types['reference']
    assert isinstance(semantic_tree, SemanticTree)
    visited = set()
    consistency_cost = 0
    for u, data in semantic_tree.tree_graph.nodes(data=True):
        node = semantic_forest.graph_nodes[data['key']]
        if isinstance(node, GroundedToken) and basic_ontology.isinstance(node.ground.type, reference):
            if node.key in visited:
                consistency_cost += 100
            else:
                visited.add(node.key)

    ontology_cost = 0
    syntax_cost = 0
    for u, v, data in semantic_tree.tree_graph.edges(data=True):
        edge_key = data['key']
        from_node = semantic_tree.tree_graph.node[u]['key']
        to_node = semantic_tree.tree_graph.node[v]['key']
        ontology_cost += semantic_forest.forest_graph[from_node][to_node][edge_key]['ontology_cost']
        syntax_cost += semantic_forest.forest_graph[from_node][to_node][edge_key]['syntax_cost']

    return 2*ontology_cost + syntax_cost