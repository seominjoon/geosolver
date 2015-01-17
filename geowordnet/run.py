from geosolver.ontology import basic_ontology
import geosolver.geowordnet.definitions as definitions
from geosolver.geowordnet.sanity_check import sanity_check

__author__ = 'minjoon'


def test_sanity_check():
    sanity_check(basic_ontology, definitions.entries, definitions.attributes, definitions.pos_types)


if __name__ == "__main__":
    test_sanity_check()
