from geosolver.ontology.load_ontology import construct_ontology_graph
from geosolver.ontology.states import Ontology

__author__ = 'minjoon'

def augment_ontology(ontology, symbols):
    '''
    :param Ontology ontology:
    :param list symbols:
    :return Ontology:
    '''
    new_symbols = ontology.symbols + symbols
    new_ontology_graph = construct_ontology_graph(new_symbols)
    new_ontology = Ontology(ontology.types, new_symbols, ontology.inheritance_graph, new_ontology_graph)
    return new_ontology
