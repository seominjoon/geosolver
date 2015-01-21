from geosolver.geowordnet.states import FunctionScorePair, EntryScorePair

__author__ = 'minjoon'


def filter_entries(geowordnet, word, threshold):
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
        score = entry.proximity_score(word)
        if score > threshold:
            pairs.append(EntryScorePair(entry, score))
    return pairs


def filter_functions(geowordnet, word, threshold):
    """
    Filter entries, and obtain the function_defs.
    Return format: {function_name: (function, score), ... }

    :param geowordnet:
    :param word:
    :param threshold:
    :return dict:
    """
    entry_score_pairs = filter_entries(geowordnet, word, threshold)
    function_score_pairs = {}

    for entry, score in entry_score_pairs:
        function_name = entry.function.name
        ssp = FunctionScorePair(entry.function, score)
        if function_name in function_score_pairs:
            if function_score_pairs[function_name].score < score:
                function_score_pairs[function_name] = ssp
        else:
            function_score_pairs[function_name] = ssp

    return function_score_pairs

