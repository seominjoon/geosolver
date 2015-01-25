from geosolver.ontology.get_ontology_paths import get_ontology_paths
from geosolver.text.semantics.get_syntax_distance_cost import get_syntax_distance_cost
from geosolver.text.semantics.states import SemanticRelation
from geosolver.text.syntax.get_syntax_paths import get_syntax_paths

__author__ = 'minjoon'


def get_semantic_relations(from_semantic_node, to_semantic_node, arg_idx):
    syntax = from_semantic_node.syntax
    basic_ontology = from_semantic_node.basic_ontology
    syntax_paths = get_syntax_paths(syntax, from_semantic_node.token, to_semantic_node.token)
    assert isinstance(syntax_paths, dict)
    syntax_path = min(syntax_paths.values(), key=lambda p: get_syntax_distance_cost(syntax, p))
    ontology_paths = get_ontology_paths(basic_ontology,
                                        from_semantic_node.function.arg_types[arg_idx], to_semantic_node.function)
    semantic_relations = {}
    for ontology_path in ontology_paths.values():
        semantic_relation = SemanticRelation(from_semantic_node, to_semantic_node, arg_idx, syntax_path, ontology_path)
        semantic_relations[semantic_relation.id] = semantic_relation

    return semantic_relations