import itertools

import networkx as nx

from geosolver.text.semantics.costs.get_ontology_path_cost import get_ontology_path_cost
from geosolver.text.semantics.costs.get_semantic_relation_cost import get_semantic_relation_cost
from geosolver.text.semantics.get_semantic_relations import get_semantic_relations
from geosolver.text.semantics.get_type_relations import get_type_relations
from geosolver.text.semantics.states import SemanticForest


__author__ = 'minjoon'

def get_semantic_forest(grounded_syntax, syntax_threshold, ontology_threshold):

    basic_ontology = grounded_syntax.basic_ontology
    grounded_tokens = grounded_syntax.grounded_tokens
    id_types = {type_.id: type_ for type_ in basic_ontology.types.values()}
    forest_graph = nx.MultiDiGraph()

    for type_ in id_types.values():
        forest_graph.add_node(type_.id, label="%s" % type_.label)

        for grounded_token in grounded_tokens.values():
            type_relations = get_type_relations(type_, grounded_token)
            for key, type_relation in type_relations.iteritems():
                syntax_cost = 0
                ontology_cost = get_ontology_path_cost(type_relation.ontology_path)
                if ontology_cost <= ontology_threshold:
                    forest_graph.add_edge(type_.id, grounded_token.key, key=key,
                                          ontology_cost=ontology_cost, syntax_cost=syntax_cost,
                                          ontology_path=type_relation.ontology_path,
                                          label="%.1f" % ontology_cost)

    for grounded_token in grounded_tokens.values():
        forest_graph.add_node(grounded_token.key, label=grounded_token.label)

    for from_token, to_token in itertools.permutations(grounded_tokens.values(), 2):
        for arg_idx in range(from_token.function.valence):
            semantic_relations = get_semantic_relations(grounded_syntax, from_token, to_token, arg_idx)
            for key, semantic_relation in semantic_relations.iteritems():
                syntax_cost, ontology_cost = get_semantic_relation_cost(semantic_relation)
                if syntax_cost <= syntax_threshold and ontology_cost <= ontology_threshold:
                    forest_graph.add_edge(from_token.key, to_token.key, key=key,
                                          arg_idx=semantic_relation.arg_idx,
                                          ontology_cost=ontology_cost, syntax_cost=syntax_cost,
                                          ontology_path=semantic_relation.ontology_path,
                                          label="%.1f, %d:%.1f" % (syntax_cost, arg_idx, ontology_cost))

    graph_nodes = dict(grounded_tokens.items() + id_types.items())
    semantic_forest = SemanticForest(grounded_syntax, graph_nodes, forest_graph)
    return semantic_forest



