from geosolver.ontology.load_ontology import _construct_ontology_graph
from geosolver.ontology.states import BasicOntology

__author__ = 'minjoon'


def augment_ontology(basic_ontology, functions):
    """
    Augments the basic_ontology with new function_defs.
    Returns the augmented basic_ontology.

    :param geosolver.basic_ontology.states.Ontology basic_ontology:
    :param dict functions:
    :return geosolver.basic_ontology.states.Ontology:
    """
    assert isinstance(basic_ontology, BasicOntology)
    assert isinstance(functions, dict)

    new_functions = dict(basic_ontology.functions.items() + functions.items())
    new_ontology_graph = _construct_ontology_graph(
        basic_ontology.types, basic_ontology.inheritance_graph, new_functions)
    new_ontology = BasicOntology(
        basic_ontology.types, new_functions, basic_ontology.inheritance_graph, new_ontology_graph)
    return new_ontology

