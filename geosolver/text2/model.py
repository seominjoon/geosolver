from collections import defaultdict, Counter
import itertools
from operator import __mul__
from sklearn.ensemble import RandomForestClassifier
from geosolver.ontology.ontology_definitions import FunctionSignature, VariableSignature, issubtype
from geosolver.ontology.ontology_definitions import signatures
from geosolver.text2.feature_function import UnaryFeatureFunction
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
    def __init__(self):
        self.tag_rules = []
        self.lexicon = defaultdict(set)

    def update(self, tag_rules):
        self.tag_rules.extend(tag_rules)
        for tag_rule in tag_rules:
            entry = (tag_rule.signature.return_type, tag_rule.signature.name)
            self.lexicon[tag_rule.get_words()].add(entry)

    def fit(self):
        pass

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
                elif word.startswith("@v"):
                    tag_rule = TagRule(syntax_parse, span, VariableSignature((span,'number'), 'number', name=word))
                    tag_rules.add(tag_rule)
                    continue

                elif word.islower() and len(word) == 1:
                    t0 = TagRule(syntax_parse, span, VariableSignature((span,'number'), 'number', name=word))
                    t1 = TagRule(syntax_parse, span, VariableSignature((span,'line'), 'line', name=word))
                    t2 = TagRule(syntax_parse, span, VariableSignature((span,'angle'), 'angle', name=word))
                    tag_rules.add(t0)
                    tag_rules.add(t1)
                    tag_rules.add(t2)
                    continue


                elif word.isupper():
                    return_types = []
                    if len(word) == 1: return_types.extend(['angle', 'point', 'circle', 'line'])
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
                        signature = VariableSignature((span,return_type), return_type, name=name)
                    tag_rule = TagRule(syntax_parse, span, signature)
                    tag_rules.add(tag_rule)
        return tag_rules

    def print_lexicon(self):
        for words, entries in self.lexicon.iteritems():
            print "%s: %s" % (" ".join(words), ", ".join(" ".join(entry) for entry in entries))



class SemanticModel(Model):
    pass

class UnaryModel(SemanticModel):
    @staticmethod
    def val_func(parent_tag_rule, child_tag_rule):
        return False

    def generate_unary_rules(self, tag_rules):
        unary_rules = set()
        for parent_tag_rule, child_tag_rule in itertools.permutations(tag_rules, 2):
            if self.__class__.val_func(parent_tag_rule, child_tag_rule):
                unary_rule = UnaryRule(parent_tag_rule, child_tag_rule)
                unary_rules.add(unary_rule)
        return unary_rules


class BinaryModel(SemanticModel):
    @staticmethod
    def val_func(parent_tag_rule, a_tag_rule, b_tag_rule):
        raise Exception()

    def generate_binary_rules(self, tag_rules):
        binary_rules = []
        for parent_tag_rule, a_tag_rule, b_tag_rule in itertools.permutations(tag_rules, 3):
            if self.__class__.val_func(parent_tag_rule, a_tag_rule, b_tag_rule):
                binary_rule = BinaryRule(parent_tag_rule, a_tag_rule, b_tag_rule)
                binary_rules.append(binary_rule)
        return binary_rules


class CombinedModel(Model):
    def __init__(self, tag_model, unary_model, core_model, is_model, cc_model):
        assert isinstance(tag_model, TagModel)
        assert isinstance(unary_model, UnaryModel)
        assert isinstance(core_model, BinaryModel)
        assert isinstance(is_model, BinaryModel)
        assert isinstance(cc_model, BinaryModel)
        self.tag_model = tag_model
        self.unary_model = unary_model
        self.core_model = core_model
        self.is_model = is_model
        self.cc_model = cc_model

    def get_score(self, rule):
        if isinstance(rule, UnaryRule):
            return self.unary_model.get_score(rule)
        elif isinstance(rule, BinaryRule):
            if rule.parent_tag_rule.signature.id == "CC":
                return self.cc_model.get_score(rule)
            elif rule.parent_tag_rule.signature.id == "Is":
                return self.is_model.get_score(rule)
            else:
                return self.core_model.get_score(rule)
        raise Exception()

    def get_tree_score(self, semantic_tree):
        assert isinstance(semantic_tree, SemanticTreeNode)
        unary_rules = semantic_tree.get_unary_rules()
        binary_rules = semantic_tree.get_binary_rules()
        scores = [self.get_score(rule) for rule in itertools.chain(unary_rules, binary_rules)]
        return reduce(__mul__, scores, 1)

    def generate_unary_rules(self, tag_rules):
        return self.unary_model.generate_unary_rules(tag_rules)

    def generate_binary_rules(self, tag_rules):
        core_rules = self.core_model.generate_binary_rules(tag_rules)
        is_rules = self.is_model.generate_binary_rules(tag_rules)
        cc_rules = self.cc_model.generate_binary_rules(tag_rules)
        out = set(itertools.chain(core_rules, is_rules, cc_rules))
        return out


class NaiveUnaryModel(UnaryModel):
    def __init__(self, max_word_distance):
        self.max_word_distance = max_word_distance

    @staticmethod
    def val_func(p, c):
        if p.signature.id in ('Is', 'CC'):
            return False
        return UnaryRule.val_func(p, c)

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


class NaiveCoreModel(NaiveBinaryModel):
    @staticmethod
    def val_func(p, a, b):
        if p.signature.id in ('Is', 'CC') or a.signature.id in ('Is', 'CC') or b.signature.id in ('Is', 'CC'):
            return False
        return BinaryRule.val_func(p, a, b)


class NaiveIsModel(NaiveBinaryModel):
    @staticmethod
    def val_func(p, a, b):
        if p.signature.id != "Is":
            return False
        if not issubtype(a.signature.return_type, b.signature.return_type) and \
                not issubtype(b.signature.return_type, a.signature.return_type):
            return False
        if not (issubtype(a.signature.return_type, 'number') or issubtype(a.signature.return_type, 'entity')):
            return False
        return BinaryRule.val_func(p, a, b)

    def get_score(self, binary_rule):
        assert isinstance(binary_rule, BinaryRule)
        b_to_a = binary_rule.syntax_parse.relation_between_spans(binary_rule.child_b_tag_rule.span,
                                                                 binary_rule.child_a_tag_rule.span, True)
        b_to_p = binary_rule.syntax_parse.relation_between_spans(binary_rule.child_b_tag_rule.span,
                                                                 binary_rule.parent_tag_rule.span, True)
        p_to_a = binary_rule.syntax_parse.relation_between_spans(binary_rule.parent_tag_rule.span,
                                                                 binary_rule.child_a_tag_rule.span, True)
        p_to_b = binary_rule.syntax_parse.relation_between_spans(binary_rule.parent_tag_rule.span,
                                                                 binary_rule.child_b_tag_rule.span, True)
        if b_to_p == "cop" and b_to_a == "nsubj":
            return 1.0
        elif p_to_a == "nsubj" and p_to_b == "dobj":
            return 1.0
        return 0.0


class NaiveCCModel(NaiveBinaryModel):
    @staticmethod
    def val_func(p, a, b):
        if p.signature.id != "CC":
            return False
        if a.signature.valence > 0:
            return False
        if b.signature.valence > 0:
            return False
        return BinaryRule.val_func(p, a, b)

    def get_score(self, binary_rule):
        assert isinstance(binary_rule, BinaryRule)
        a_to_b = binary_rule.syntax_parse.relation_between_spans(binary_rule.child_a_tag_rule.span,
                                                                 binary_rule.child_b_tag_rule.span, True)
        a_to_p = binary_rule.syntax_parse.relation_between_spans(binary_rule.child_a_tag_rule.span,
                                                                 binary_rule.parent_tag_rule.span, True)
        if a_to_p == "cc" and (a_to_b == "conj" or a_to_b == "advmod"):
            return 1.0
        return 0.0


class RFUnaryModel(UnaryModel):
    def __init__(self):
        self.positive_unary_rules = []
        self.negative_unary_rules = []
        self.feature_function = None
        self.classifier = RandomForestClassifier()

    @staticmethod
    def val_func(p, c):
        if p.signature.id in ('Is', 'CC'):
            return False
        return UnaryRule.val_func(p, c)

    def update(self, tag_rules, positive_unary_rules):
        all_unary_rules = self.generate_unary_rules(tag_rules)
        negative_unary_rules = all_unary_rules - positive_unary_rules
        self.positive_unary_rules.extend(positive_unary_rules)
        self.negative_unary_rules.extend(negative_unary_rules)

    def fit(self):
        print "# of positive unary examples:", len(self.positive_unary_rules)
        print "# of negative unary examples:", len(self.negative_unary_rules)
        self.feature_function = UnaryFeatureFunction(self.positive_unary_rules)
        X = []
        y = []
        for pur in self.positive_unary_rules:
            X.append(self.feature_function.map(pur))
            y.append(1)
        for nur in self.negative_unary_rules:
            X.append(self.feature_function.map(nur))
            y.append(0)

        print "length of unary feature vector:", np.shape(X)[1]
        self.classifier.fit(X, y)

    def get_score(self, ur):
        x = self.feature_function.map(ur)
        probas = self.classifier.predict_proba([x])
        return probas[0][1]



