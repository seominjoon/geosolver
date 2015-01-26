from geosolver.ontology.get_ontology_paths import get_ontology_paths
from geosolver.text.semantics.states import TypeRelation

__author__ = 'minjoon'

def get_type_relations(from_type, to_grounded_token):
    ontology_paths = get_ontology_paths(to_grounded_token.basic_ontology,
                                        from_type, to_grounded_token.function)

    type_relations = {}
    for ontology_path in ontology_paths.values():
        type_relation = TypeRelation(from_type, to_grounded_token, ontology_path)
        type_relations[type_relation.key] = type_relation

    return type_relations
