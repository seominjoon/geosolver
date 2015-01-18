from collections import namedtuple

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

    EntryScorePair = namedtuple('EntryScorePair', 'entry score')

    pairs = []
    for entry in geowordnet.entries:
        score = entry.proximity_score(word)
        if score > threshold:
            pairs.append(EntryScorePair(entry, score))
    return pairs


def filter_symbols(geowordnet, word, threshold):
    """
    Filter entries, and obtain the symbols.
    Return format: {symbol_name: (symbol, score), ... }

    :param geowordnet:
    :param word:
    :param threshold:
    :return dict:
    """

    SymbolScorePair = namedtuple('SymbolScorePair', 'symbol score')

    entry_score_pairs = filter_entries(geowordnet, word, threshold)
    symbol_score_pairs = {}

    for entry, score in entry_score_pairs:
        symbol_name = entry.symbol.name
        ssp = SymbolScorePair(entry.symbol, score)
        if symbol_name in symbol_score_pairs:
            if symbol_score_pairs[symbol_name].score < score:
                symbol_score_pairs[symbol_name] = ssp
        else:
            symbol_score_pairs[symbol_name] = ssp

    return symbol_score_pairs

