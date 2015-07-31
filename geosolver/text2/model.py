from collections import defaultdict, Counter
from geosolver.text2.rule import TagRule

__author__ = 'minjoon'

def _normalize(counter):
    n = len(counter)
    new_counter = Counter({key: float(value) for key, value in counter.iteritems()})
    return new_counter


class Model(object):
    def __init__(self, rules, feature_func):
        self.rules = rules
        self.feature_func = feature_func

class TagModel(Model):
    def predict(self, syntax_parse, span):
        pass

class NaiveTagModel(TagModel):
    """
    Stores mapping for each phrase (lexicon).
    Upon predict, give probability based on counting
    """
    def __init__(self, tag_rules):
        super(NaiveTagModel, self).__init__(tag_rules, None)
        self.lexicon = defaultdict(lambda: Counter())
        for tag_rule in tag_rules:
            self.lexicon[tag_rule.get_words()][tag_rule.signatue] += 1

    def predict(self, syntax_parse, span):
        signature_counter = self.lexicon[syntax_parse.get_words(span)]
        tag_counter = Counter({TagRule(syntax_parse, span, signature): count
                               for signature, count in signature_counter.iteritems()})
        tag_dist = _normalize(tag_counter)
        return tag_dist

class SemanticModel(Model):
    def get_prob(self, semantic_rule):
        pass


class UnaryModel(SemanticModel):
    def __init__(self, unary_rules, feature_func):
        super(UnaryModel, self).__init__(unary_rules, feature_func)

    def get_prob(self, semantic_rule):
        return 1.0