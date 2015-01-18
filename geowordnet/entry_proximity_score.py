import nltk
import inflect

__author__ = 'minjoon'

inflect_engine = inflect.engine()


def entry_proximity_score(word, entry):
    """
    Given word and an entry, returns proximity between the word and the entry.
    If the word equals the lemma of the entry, then score is 1.
    Otherwise, use edit distance.

    :param geosolver.geowordnet.states.Entry entry:
    :param str word:
    :return float:
    """
    if inflect_engine.compare(word, entry.lemma):
        return 1
    else:
        distance = nltk.metrics.edit_distance(word, entry.lemma)
        sum_len = len(word) + len(entry.lemma)
        return float(sum_len-distance)/sum_len
