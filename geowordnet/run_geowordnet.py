from geosolver.geowordnet.entry_proximity_score import entry_proximity_score
from geosolver.geowordnet.filters import filter_functions
from geosolver.geowordnet.new_function_identifier import new_function_identifier
from geosolver.ontology import basic_ontology, ontology_semantics
import geosolver.geowordnet.definitions as definitions
from geosolver.geowordnet.sanity_check import sanity_check
from geosolver.geowordnet import geowordnet

__author__ = 'minjoon'


def test_sanity_check():
    sanity_check(definitions.entries, definitions.attributes, definitions.pos_types)


def test_entry_proximity_score():
    entry = geowordnet.entries[0]
    print(entry)
    print(entry.proximity_score('add'))


def test_function_identifier():
    print(new_function_identifier(basic_ontology, ontology_semantics, "a"))


def test_filters():
    print(filter_functions(ontology_semantics, geowordnet, entry_proximity_score, new_function_identifier,
                           '5', 0.7))


if __name__ == "__main__":
    # test_sanity_check()
    # test_entry_proximity_score()
    # test_filters()
    test_function_identifier()
