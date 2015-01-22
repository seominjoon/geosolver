from geosolver.geowordnet.states import EntryScorePair, FunctionScorePair

__author__ = 'minjoon'



def filter_entries(geowordnet, proximity_score_function, word, threshold):
    """
    Given word, finds entries whose entry proximity score with the word is higher than the threshold.
    Return format: [(entry, score), ...]

    :param geowordnet:
    :param word:
    :param threshold:
    :return list:
    """
    pairs = []
    for entry in geowordnet.entries:
        score = proximity_score_function(word, entry)
        if score > threshold:
            pairs.append(EntryScorePair(entry, score))
    return pairs


def filter_functions(ontology_semantics, geowordnet,
                     proximity_score_function, new_function_identifier, word, threshold):
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
    entry_score_pairs = filter_entries(geowordnet, proximity_score_function, word, threshold)

    for entry, score in entry_score_pairs:
        function_name = entry.function.name
        fsp = FunctionScorePair(entry.function, score)
        if function_name in function_score_pairs:
            if function_score_pairs[function_name].score < score:
                function_score_pairs[function_name] = fsp
        else:
            function_score_pairs[function_name] = fsp

    # From new_function identifier
    for name, fsp in new_function_identifier(geowordnet.basic_ontology, ontology_semantics, word).iteritems():
        function_score_pairs[name] = fsp

    return function_score_pairs

