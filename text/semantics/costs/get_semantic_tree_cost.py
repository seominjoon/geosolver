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
        if isinstance(node, GroundedToken) and basic_ontology.isinstance(node.function.return_type, reference):
            if node.key in visited:
                consistency_cost += 100
            else:
                visited.add(node.key)

    return consistency_cost + 2*semantic_tree.ontology_cost + semantic_tree.grounded_syntax_cost