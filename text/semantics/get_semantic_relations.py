from geosolver.ontology.get_ontology_paths import get_ontology_paths
from geosolver.ontology.states import OntologyPath
from geosolver.text.semantics.get_syntax_path_cost import get_syntax_path_cost
from geosolver.text.semantics.states import SemanticRelation
from geosolver.text.syntax.get_syntax_paths import get_syntax_paths

__author__ = 'minjoon'


def get_semantic_relations(from_semantic_node, to_semantic_node, arg_idx):
    syntax = from_semantic_node.syntax
    basic_ontology = from_semantic_node.basic_ontology
    semantic_relations = {}
    syntax_paths = get_syntax_paths(syntax, from_semantic_node.token, to_semantic_node.token)
    if len(syntax_paths) == 0:
        return semantic_relations

    syntax_path = min(syntax_paths.values(), key=lambda p: get_syntax_path_cost(syntax, p))
    ontology_paths = get_ontology_paths(basic_ontology,
                                        from_semantic_node.function.arg_types[arg_idx], to_semantic_node.function)
    for ontology_path in ontology_paths.values():
        augmented_ontology_path = OntologyPath(basic_ontology, [from_semantic_node]+ontology_path.path_nodes,
                                               ontology_path.key)
        semantic_relation = SemanticRelation(from_semantic_node, to_semantic_node, arg_idx, syntax_path,
                                             augmented_ontology_path)
        semantic_relations[semantic_relation.id] = semantic_relation

    return semantic_relations