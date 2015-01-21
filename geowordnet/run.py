from geosolver.geowordnet.entry_proximity_score import entry_proximity_score
from geosolver.ontology import basic_ontology
import geosolver.geowordnet.definitions as definitions
from geosolver.geowordnet.sanity_check import sanity_check
from geosolver.geowordnet import geowordnet

__author__ = 'minjoon'


def test_sanity_check():
    sanity_check(basic_ontology, definitions.entries, definitions.attributes, definitions.pos_types)


def test_entry_proximity_score():
    entry = geowordnet.entries[0]
    print(entry)
    print(entry.proximity_score('add'))


def test_filters():
    print(geowordnet.filter_functions('radius', 0.7))


if __name__ == "__main__":
    # test_sanity_check()
    # test_entry_proximity_score()
    test_filters()
