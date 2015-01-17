from geosolver.ontology.load_ontology import _construct_ontology_graph
from geosolver.ontology.states import BasicOntology

__author__ = 'minjoon'


def augment_ontology(ontology, symbols):
    """
    Augments the ontology with new symbols.
    Returns the augmented ontology.

    :param geosolver.ontology.states.Ontology ontology:
    :param list symbols:
    :return geosolver.ontology.states.Ontology:
    """
    new_symbols = dict(ontology.symbols.items() + [(symbol_.name, symbol_) for symbol_ in symbols])
    new_ontology_graph = _construct_ontology_graph(ontology.inheritance_graph, new_symbols)
    new_ontology = BasicOntology(ontology.types, new_symbols, ontology.inheritance_graph, new_ontology_graph)
    return new_ontology

