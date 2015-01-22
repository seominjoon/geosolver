import re
from geosolver.geowordnet.states import FunctionScorePair
from geosolver.ontology.states import Function, BasicOntology

"""
There are infinite number of "number" functions and "reference" functions.
Instead of deining entries for these, we have an identifier for them using regex.
This will NOT be included in GeoWordNet; instead like proximity score, this needs to be called separately.
"""

__author__ = 'minjoon'


def new_function_identifier(basic_ontology, ontology_semantics, word):
    """
    Returns a dictionary of function-score pairs that the word might refer to,
    in the domain of number and reference.
    These functions will be added to the ontology to create new ontology.
    For now, ontology semantics is not used, but later, this needs to be used to instantiate new functions,
    as the names have to make sense in the semantics.

    :param BasicOntology basic_ontology:
    :param OntologySemantics ontology_semantics:
    :param word:
    :return:
    """
    assert isinstance(basic_ontology, BasicOntology)

    number_score = _get_number_score(word)
    reference_score = _get_reference_score(word)

    pairs = {}

    if number_score > 0 and reference_score > 0:
        raise Exception("?")

    elif number_score > 0:
        function = Function(word, [basic_ontology.types['ground']], basic_ontology.types['number'])
        pair = FunctionScorePair(function, number_score)
        pairs[word] = pair

    elif reference_score > 0:
        function = Function(word, [basic_ontology.types['ground']], basic_ontology.types['reference'])
        pair = FunctionScorePair(function, reference_score)
        pairs[word] = pair

    return pairs


def _get_number_score(word):
    """
    If word can be a number, returns a dictionary of normalized number with score.

    :param word:
    :return:
    """
    regex1 = re.compile("^\d+(.\d+)?$")
    score1 = 1.0

    if regex1.match(word):
        return score1
    else:
        return 0


def _get_reference_score(word):
    """
    if word can be a reference, returns a dictionary of normalized reference with score.

    :param word:
    :return:
    """
    regex1 = re.compile("^([B-Z])|([A-Z][A-Z]+)$")
    regex2 = re.compile("^A$")
    regex3 = re.compile("^[b-z](_[a-z0-9])?$")
    score1 = 1.0
    score2 = 0.5
    score3 = 1.0

    if regex1.match(word):
        return score1
    elif regex2.match(word):
        return score2
    elif regex3.match(word):
        return score3
    else:
        return 0

