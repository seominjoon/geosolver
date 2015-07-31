from collections import defaultdict, Counter
from geosolver.ontology.ontology_definitions import FunctionSignature, VariableSignature
from geosolver.ontology.ontology_definitions import signatures
from geosolver.text2.rule import TagRule
from geosolver.utils.num import is_number

__author__ = 'minjoon'

def _normalize(counter):
    n = len(counter)
    new_counter = Counter({key: float(value) for key, value in counter.iteritems()})
    return new_counter


class Model(object):
    def __init__(self, rules, feature_func):
        self.rules = rules
        self.feature_func = feature_func

    def get_score(self, rule):
        return 0.0

class TagModel(Model):
    pass

class NaiveTagModel(TagModel):
    """
    It predicts 0 for unseen tag rule, and 1 for seen.
    """
    def __init__(self, tag_rules):
        super(NaiveTagModel, self).__init__(tag_rules, None)
        self.lexicon = defaultdict(set)
        for tag_rule in tag_rules:
            entry = (tag_rule.signature.return_type, tag_rule.signature.name)
            """
            if tag_rule.get_words()[0] == "of" and entry[0] == "number":
                raise Exception()
            """
            self.lexicon[tag_rule.get_words()].add(entry)

    def get_score(self, tag_rule):
        words = tag_rule.get_words()
        if words in self.lexicon and tag_rule.signature.name in self.lexicon[words]:
            return 1.0
        return 0.0

    def generate_tag_rules(self, syntax_parse):
        tag_rules = set()
        for span in syntax_parse.iterate_spans():
            words = syntax_parse.get_words(span)
            if len(words) == 1:
                word = words[0]
                if is_number(word):
                    tag_rule = TagRule(syntax_parse, span, FunctionSignature(word, 'number', []))
                    tag_rules.add(tag_rule)
                    continue
                elif word.startswith("@v") or (word.islower() and len(word) == 1):
                    tag_rule = TagRule(syntax_parse, span, VariableSignature((span,'number'), 'number', name=word))
                    tag_rules.add(tag_rule)
                    continue

                elif word.isupper():
                    return_types = []
                    if len(word) == 1: return_types.extend(['angle', 'point'])
                    elif len(word) == 2: return_types.extend(['number', 'line', 'arc'])
                    elif len(word) == 3: return_types.extend(['angle', 'triangle', 'number'])
                    elif len(word) == 4: return_types.extend(['quad'])
                    elif len(word) == 6: return_types.extend(['hexagon'])
                    else: return_types.extend(['polygon'])
                    curr_tag_rules = [TagRule(syntax_parse, span, VariableSignature((span,rt), rt, name=word))
                                      for rt in return_types]
                    for tag_rule in curr_tag_rules: tag_rules.add(tag_rule)
                    continue

            if words in self.lexicon:
                for return_type, name in self.lexicon[words]:
                    if name[0].isupper():
                        signature = signatures[name]
                    else:
                        signature = VariableSignature(name, return_type)
                    tag_rule = TagRule(syntax_parse, span, signature)
                    tag_rules.add(tag_rule)
        return tag_rules

    def print_lexicon(self):
        for words, entries in self.lexicon.iteritems():
            print "%s: %s" % (" ".join(words), ", ".join(" ".join(entry) for entry in entries))



class SemanticModel(Model):
    pass

class UnaryModel(SemanticModel):
    def __init__(self, unary_rules, feature_func):
        super(UnaryModel, self).__init__(unary_rules, feature_func)

    def get_score(self, semantic_rule):
        return 1.0