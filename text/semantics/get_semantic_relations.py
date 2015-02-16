from geosolver.ontology.get_ontology_paths import get_ontology_paths
from geosolver.ontology.states import OntologyPath
from geosolver.text.token_grounding.get_grounded_syntax_paths import get_grounded_syntax_paths
from geosolver.text.semantics.costs.get_grounded_syntax_path_cost import get_grounded_syntax_path_cost
from geosolver.text.semantics.states import SemanticRelation

__author__ = 'minjoon'


def get_semantic_relations(grounded_syntax, from_grounded_token, to_grounded_token, arg_idx):
    basic_ontology = grounded_syntax.basic_ontology
    semantic_relations = {}
    grounded_syntax_paths = get_grounded_syntax_paths(grounded_syntax, from_grounded_token, to_grounded_token)
    if len(grounded_syntax_paths) == 0:
        return semantic_relations

    grounded_syntax_path = min(grounded_syntax_paths.values(),
                               key=lambda p: get_grounded_syntax_path_cost(p))
    ontology_paths = get_ontology_paths(basic_ontology,
                                        from_grounded_token.ground.arg_types[arg_idx],
                                        to_grounded_token.ground)
    for ontology_path in ontology_paths.values():
        augmented_ontology_path = OntologyPath(basic_ontology,
                                               [from_grounded_token.ground]+ontology_path.path_nodes,
                                               ontology_path.key)
        semantic_relation = SemanticRelation(from_grounded_token, to_grounded_token, arg_idx,
                                             grounded_syntax_path, augmented_ontology_path)
        semantic_relations[semantic_relation.key] = semantic_relation

    return semantic_relations
