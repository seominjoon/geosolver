from geosolver.ontology.get_ontology_paths import get_ontology_paths
from geosolver.text.semantics.states import SourceRelation

__author__ = 'minjoon'

def get_source_relations(from_source_node, to_semantic_node):
    ontology_paths = get_ontology_paths(to_semantic_node.basic_ontology,
                                        from_source_node.type, to_semantic_node.function)
    source_relations = {}
    for ontology_path in ontology_paths.values():
        source_relation = SourceRelation(from_source_node, to_semantic_node, ontology_path)
        source_relations[source_relation.id] = source_relation

    return source_relations