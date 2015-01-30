import itertools

import networkx as nx

from geosolver.text.semantics.costs.get_ontology_path_cost import get_ontology_path_cost
from geosolver.text.semantics.costs.get_semantic_relation_cost import get_semantic_relation_cost
from geosolver.text.semantics.get_semantic_relations import get_semantic_relations
from geosolver.text.semantics.get_type_relations import get_type_relations
from geosolver.text.semantics.states import SemanticForest, ImpliedInstance, ImpliedParentFunction

__author__ = 'minjoon'


def get_semantic_forest(grounded_syntax, syntax_threshold, ontology_threshold):

    basic_ontology = grounded_syntax.basic_ontology
    grounded_tokens = grounded_syntax.grounded_tokens

    # Populating forest graph
    forest_graph = nx.MultiDiGraph()
    forest_graph = _add_types(grounded_syntax, forest_graph)
    forest_graph = _add_grounded_tokens(grounded_syntax, forest_graph)
    forest_graph = _add_type_relations(grounded_syntax, forest_graph, ontology_threshold)
    forest_graph = _add_semantic_relations(grounded_syntax, forest_graph, syntax_threshold, ontology_threshold)
    implied_instances = _get_implied_instances(grounded_syntax)
    implied_parent_functions = _get_implied_parent_functions(grounded_syntax, basic_ontology.types['equal'])
    forest_graph = _add_implied_instances(forest_graph, implied_instances)
    forest_graph = _add_implied_parent_functions(forest_graph, implied_parent_functions)
    forest_graph = _add_implied_instance_relations(forest_graph, implied_instances)
    forest_graph = _add_implied_parent_function_relations(forest_graph, implied_parent_functions)

    graph_nodes = dict(grounded_tokens.items() + basic_ontology.types_by_id.items() +
                       implied_instances.items() + implied_parent_functions.items())
    semantic_forest = SemanticForest(grounded_syntax, graph_nodes, forest_graph)
    return semantic_forest


def _add_types(grounded_syntax, forest_graph):
    basic_ontology = grounded_syntax.basic_ontology
    forest_graph = forest_graph.copy()
    for type_ in basic_ontology.types.values():
        forest_graph.add_node(type_.id, label="%s" % type_.label)
    return forest_graph


def _add_type_relations(grounded_syntax, forest_graph, ontology_threshold):
    basic_ontology = grounded_syntax.basic_ontology
    grounded_tokens = grounded_syntax.grounded_tokens
    forest_graph = forest_graph.copy()

    for type_ in basic_ontology.types.values():
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
    return forest_graph


def _add_grounded_tokens(grounded_syntax, forest_graph):
    grounded_tokens = grounded_syntax.grounded_tokens
    forest_graph = forest_graph.copy()
    for grounded_token in grounded_tokens.values():
        forest_graph.add_node(grounded_token.key, label=grounded_token.label)
    return forest_graph


def _add_semantic_relations(grounded_syntax, forest_graph, syntax_threshold, ontology_threshold):
    grounded_tokens = grounded_syntax.grounded_tokens
    forest_graph = forest_graph.copy()

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
    return forest_graph


def _add_implied_instances(forest_graph, implied_instances):
    forest_graph = forest_graph.copy()
    for implied_instance in implied_instances.values():
        forest_graph.add_node(implied_instance.key, label=implied_instance.label)
    return forest_graph


def _add_implied_parent_functions(forest_graph, implied_parent_functions):
    forest_graph = forest_graph.copy()
    for implied_parent_function in implied_parent_functions.values():
        forest_graph.add_node(implied_parent_function.key, label=implied_parent_function.label)
    return forest_graph


def _add_implied_instance_relations(forest_graph, implied_instances):
    forest_graph = forest_graph.copy()
    for implied_instance in implied_instances.values():
        # Needs to initialize these vallues
        syntax_cost = 0
        ontology_cost = 0

        parent_grounded_token = implied_instance.parent_ground_token
        forest_graph.add_edge(parent_grounded_token.key, implied_instance.key,
                              arg_idx=implied_instance.arg_idx,
                              ontology_cost=ontology_cost, syntax_cost=syntax_cost,
                              label="%.1f, %d:%.1f" % (syntax_cost, 0, ontology_cost))
    return forest_graph


def _add_implied_parent_function_relations(forest_graph, implied_parent_functions):
    forest_graph = forest_graph.copy()
    for implied_parent_function in implied_parent_functions.values():
        syntax_cost = 0  # calculate by averaging distances between children.
        ontology_cost = 0
        for arg_idx, child_ground_token in enumerate(implied_parent_function.child_ground_tokens):
            forest_graph.add_edge(implied_parent_function.key, child_ground_token.key,
                                  arg_idx=arg_idx,
                                  ontology_cost=ontology_cost, syntax_cost=syntax_cost,
                                  label="%.1f, %d:%.1f" % (syntax_cost, arg_idx, ontology_cost))
    return forest_graph


def _get_implied_instances(grounded_syntax):
    """
    For each arg_idx of each grounded token, create implied instance
    :param grounded_syntax:
    :param forest_graph:
    :return:
    """
    implied_instances = {}
    grounded_tokens = grounded_syntax.grounded_tokens
    for grounded_token in grounded_tokens.values():
        function = grounded_token.function
        for arg_idx, type_ in enumerate(function.arg_types):
            implied_instance = ImpliedInstance(grounded_token, arg_idx, type_)
            implied_instances[implied_instance.key] = implied_instance
    return implied_instances


def _get_implied_parent_functions(grounded_syntax, function):
    """
    Given function, enumerate over all possible combinations of grounded tokens and
    create unique implied function for each combination.
    :param grounded_syntax:
    :param function:
    :return:
    """
    implied_parent_functions = {}
    grounded_tokens = grounded_syntax.grounded_tokens

    for arg_tokens in itertools.permutations(grounded_tokens.values(), function.valence):
        if _match(function, arg_tokens):
            implied_parent_function = ImpliedParentFunction(function, arg_tokens)
            implied_parent_functions[implied_parent_function.key] = implied_parent_function
    return implied_parent_functions


def _match(function, arg_tokens):
    for arg_idx, arg_token in enumerate(arg_tokens):
        if function.arg_types[arg_idx] != arg_token.function.return_type:
            return False
    return True
