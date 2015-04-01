from geosolver.geowordnet.definitions import entries
from geosolver.geowordnet.load_geowordnet import load_geowordnet
from geosolver.ontology import basic_ontology

__author__ = 'minjoon'

geowordnet = load_geowordnet(basic_ontology, entries)
