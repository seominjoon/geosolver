from collections import defaultdict, Counter
import itertools
from operator import __mul__
from geosolver.ontology.ontology_definitions import FunctionSignature, VariableSignature
from geosolver.ontology.ontology_definitions import signatures
from geosolver.text2.rule import TagRule, UnaryRule, BinaryRule
from geosolver.text2.semantic_tree import SemanticTreeNode
from geosolver.utils.num import is_number
import numpy as np

__author__ = 'minjoon'

def _normalize(counter):
    n = len(counter)
    new_counter = Counter({key: float(value) for key, value in counter.iteritems()})
    return new_counter


class Model(object):
    def get_score(self, rule):
        return 0.0

class TagModel(Model):
    pass

class NaiveTagModel(TagModel):
    """
    It predicts 0 for unseen tag rule, and 1 for seen.
    """
    def __init__(self, tag_rules):
        self.tag_rules = tag_rules
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
    def generate_unary_rules(self, tag_rules):
        unary_rules = []
        for parent_tag_rule, child_tag_rule in itertools.permutations(tag_rules, 2):
            if UnaryRule.check_validity(parent_tag_rule, child_tag_rule):
                unary_rule = UnaryRule(parent_tag_rule, child_tag_rule)
                unary_rules.append(unary_rule)
        return unary_rules

class BinaryModel(SemanticModel):
    def generate_binary_rules(self, tag_rules):
        binary_rules = []
        for parent_tag_rule, a_tag_rule, b_tag_rule in itertools.permutations(tag_rules, 3):
            if BinaryRule.check_validity(parent_tag_rule, a_tag_rule, b_tag_rule):
                binary_rule = BinaryRule(parent_tag_rule, a_tag_rule, b_tag_rule)
                binary_rules.append(binary_rule)
        return binary_rules

class UnifiedModel(Model):
    def __init__(self, unary_model, binary_model):
        self.unary_model = unary_model
        self.binary_model = binary_model

    def get_score(self, rule):
        if isinstance(rule, UnaryRule):
            return self.unary_model.get_score(rule)
        elif isinstance(rule, BinaryRule):
            return self.binary_model.get_score(rule)
        raise Exception()

    def get_tree_score(self, semantic_tree):
        assert isinstance(semantic_tree, SemanticTreeNode)
        unary_rules = semantic_tree.get_unary_rules()
        binary_rules = semantic_tree.get_binary_rules()
        scores = [self.get_score(rule) for rule in itertools.chain(unary_rules, binary_rules)]
        return reduce(__mul__, scores, 1)


class NaiveUnaryModel(UnaryModel):
    def __init__(self, max_word_distance):
        self.max_word_distance = max_word_distance

    def get_score(self, unary_rule):
        assert isinstance(unary_rule, UnaryRule)
        syntax_parse = unary_rule.syntax_parse
        distance = syntax_parse.distance_between_spans(unary_rule.child_tag_rule.span, unary_rule.parent_tag_rule.span)
        if distance == 0:
            return 1.0
        if distance > self.max_word_distance:
            return 0.0
        return 1.0/distance


class NaiveBinaryModel(BinaryModel):
    def __init__(self, max_word_distance):
        self.max_word_distance = max_word_distance

    def get_score(self, binary_rule):
        assert isinstance(binary_rule, BinaryRule)
        syntax_parse = binary_rule.syntax_parse
        da = syntax_parse.distance_between_spans(binary_rule.child_a_tag_rule.span, binary_rule.parent_tag_rule.span)
        db = syntax_parse.distance_between_spans(binary_rule.child_b_tag_rule.span, binary_rule.parent_tag_rule.span)
        if da == 0: sa = 1
        elif da > self.max_word_distance: sa = 0
        else: sa = 1.0/da
        if db == 0: sb = 1
        elif db > self.max_word_distance: sb = 0
        else: sb = 1.0/db
        return np.mean([sa, sb])

class RFUnaryModel(UnaryModel):
    def __init__(self):
        self.positive_unary_rules = []
        self.negative_unary_rules = []

    def update(self, tag_rules, positive_unary_rules):
        pass