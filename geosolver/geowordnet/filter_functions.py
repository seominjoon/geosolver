from geosolver.geowordnet.get_lexical_matching_score import get_lexical_matching_score
from geosolver.geowordnet.identify_constants import identify_constants
from geosolver.geowordnet.states import EntryScorePair, FunctionScorePair

__author__ = 'minjoon'


def filter_functions(ontology_semantics, geowordnet, word, threshold):
    """
    Filter entries, and obtain the function_defs.
    Return format: {function_name: (function, score), ... }
    Might instantiate new functions to be added to the ontology.

    :param geowordnet:
    :param word:
    :param threshold:
    :return dict:
    """
    function_score_pairs = {}

    # From entries
    entry_score_pairs = _filter_entries(geowordnet, get_lexical_matching_score, word, threshold)

    for entry, score in entry_score_pairs:
        function_name = entry.function.name
        fsp = FunctionScorePair(entry.function, score)
        if function_name in function_score_pairs:
            if function_score_pairs[function_name].score < score:
                function_score_pairs[function_name] = fsp
        else:
            function_score_pairs[function_name] = fsp

    # From new_function identifier; case might matter here.
    """
    for name, fsp in identify_constants(geowordnet.basic_ontology, ontology_semantics, word).iteritems():
        function_score_pairs[name] = fsp
    """
    return function_score_pairs


def _filter_entries(geowordnet, get_lexical_matching_score, word, threshold):
    """
    Given word, finds entries whose entry proximity score with the word is higher than the threshold.
    Return format: [(entry, score), ...]

    :param geowordnet:
    :param word:
    :param threshold:
    :return list:
    """
    word = word.lower()  # case shouldn't matter here
    pairs = []
    for entry in geowordnet.entries:
        score = get_lexical_matching_score(word, entry)
        if score > threshold:
            pairs.append(EntryScorePair(entry, score))
    return pairs


