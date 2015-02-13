import inflect
from geosolver.geowordnet.get_lexical_matching_score import get_lexical_matching_score
from geosolver.geowordnet.filter_functions import filter_functions
from geosolver.geowordnet.identify_constants import identify_constants
from geosolver.ontology import basic_ontology, ontology_semantics
import geosolver.geowordnet.definitions as definitions
from geosolver.geowordnet.sanity_check import sanity_check
from geosolver.geowordnet import geowordnet

__author__ = 'minjoon'


def test_sanity_check():
    sanity_check(definitions.entries, definitions.attributes, definitions.pos_types)


def test_get_lexical_matching_score():
    entry = geowordnet.entries[0]
    print(entry)
    print(get_lexical_matching_score('adds', entry))


def test_new_function_identifier():
    print(identify_constants(basic_ontology, ontology_semantics, "ABC"))


def test_filters():
    print(filter_functions(ontology_semantics, geowordnet, 'bisects', 0.7))


if __name__ == "__main__":
    # test_sanity_check()
    # test_get_lexical_matching_score()
    test_filters()
    # test_new_function_identifier()
