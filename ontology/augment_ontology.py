from geosolver.ontology.load_ontology import _construct_ontology_graph
from geosolver.ontology.states import BasicOntology

__author__ = 'minjoon'


def augment_ontology(ontology, functions):
    """
    Augments the ontology with new function_defs.
    Returns the augmented ontology.

    :param geosolver.ontology.states.Ontology ontology:
    :param list function_defs:
    :return geosolver.ontology.states.Ontology:
    """
    assert isinstance(ontology, BasicOntology)

    new_functions = dict(ontology.functions.items() + [(function.name, function) for function in functions])
    new_ontology_graph = _construct_ontology_graph(ontology.inheritance_graph, new_functions)
    new_ontology = BasicOntology(ontology.types, new_functions, ontology.inheritance_graph, new_ontology_graph)
    return new_ontology

