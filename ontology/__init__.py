from geosolver.ontology import basic_definitions
from geosolver.ontology.load_ontology import load_ontology

__author__ = 'minjoon'

basic_ontology = load_ontology(basic_definitions.type_defs, basic_definitions.function_defs)
ontology_semantics = None
