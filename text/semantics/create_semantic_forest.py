import networkx as nx
import itertools
from geosolver.text.semantics.get_semantic_relation_cost import get_semantic_relation_cost
from geosolver.text.semantics.get_semantic_relations import get_semantic_relations
from geosolver.text.semantics.get_ontology_path_cost import get_ontology_path_cost
from geosolver.text.semantics.get_source_relations import get_source_relations
from geosolver.text.semantics.states import SemanticForest, SemanticNode, SourceNode

__author__ = 'minjoon'


def create_semantic_forest(semantic_nodes, syntax_threshold, ontology_threshold):
    assert isinstance(semantic_nodes, dict)

    any_node = semantic_nodes.values()[0]
    assert isinstance(any_node, SemanticNode)

    syntax = any_node.syntax
    basic_ontology = any_node.basic_ontology
    source_nodes = _create_source_nodes(basic_ontology)

    forest_graph = nx.MultiDiGraph()

    for source_node in source_nodes.values():
        forest_graph.add_node(source_node.id, label="%s" % source_node.label)

        for semantic_node in semantic_nodes.values():
            source_relations = get_source_relations(source_node, semantic_node)
            for source_relation in source_relations.values():
                syntax_cost = 0
                ontology_cost = get_ontology_path_cost(basic_ontology, source_relation.ontology_path)
                if ontology_cost <= ontology_threshold:
                    forest_graph.add_edge(source_node.id, semantic_node.id, key=source_relation.key,
                                          ontology_cost=ontology_cost, syntax_cost=syntax_cost,
                                          label="%.1f" % ontology_cost)

    for node in semantic_nodes.values():
        forest_graph.add_node(node.id, label=node.label)

    for from_node, to_node in itertools.permutations(semantic_nodes.values(), 2):
        for arg_idx in range(from_node.function.valence):
            semantic_relations = get_semantic_relations(from_node, to_node, arg_idx)
            for semantic_relation in semantic_relations.values():
                syntax_cost, ontology_cost = get_semantic_relation_cost(semantic_relation)
                if syntax_cost <= syntax_threshold and ontology_cost <= ontology_threshold:
                    forest_graph.add_edge(from_node.id, to_node.id, key=semantic_relation.key,
                                          ontology_cost=ontology_cost, syntax_cost=syntax_cost,
                                          label="%d:%.1f, %.1f" % (arg_idx, syntax_cost, ontology_cost))

    semantic_forest = SemanticForest(syntax, basic_ontology, source_nodes, semantic_nodes, forest_graph)
    return semantic_forest


def _create_source_nodes(basic_ontology):
    source_nodes = {}
    for type_ in basic_ontology.types.values():
        source_node = SourceNode(type_)
        source_nodes[source_node.id] = source_node
    return source_nodes
