import itertools
import numpy as np
import re
from geosolver.text.ontology import function_signatures
from geosolver.text.ontology_states import FunctionSignature

__author__ = 'minjoon'

class TagModel(object):
    def __init__(self):
        pass

    def get_log_distribution(self, word):
        """
        TO BE OVERRIDDEN

        :param words:
        :param syntax_tree:
        :param index:
        :return:
        """
        pass

    def get_best_tag(self, word):
        dist = self.get_log_distribution(word)
        return max(dist.items(), key=lambda x: x[1])

    def get_best_tags(self, words):
        tags = {index: self.get_best_tag(words[index])[0] for index in words.keys()}
        return tags

    def get_log_combinations(self, words):
        combinations = []
        indices = words.keys()
        distributions = [self.get_log_distribution(words[index]) for index in indices]
        for pairs in itertools.product(*distributions):
            tags = {indices[index]: pair[0] for index, pair in enumerate(pairs) if pair[0] is not None}
            prob = sum(pair[1] for pair in pairs if pair[0] is not None)
            combinations.append((tags, prob))
        return combinations


class CountBasedTagModel(TagModel):
    def __init__(self, tag_rules):
        self.tag_rules = tag_rules
        self.counter = {}
        self._sum_key = '$'
        for tag_rule in tag_rules:
            if tag_rule.index is None:
                continue
            word = tag_rule.words[tag_rule.index]
            signature = tag_rule.signature
            if word not in self.counter:
                self.counter[word] = {}
                self.counter[word][self._sum_key] = 0
            if signature not in self.counter[word]:
                self.counter[word][signature] = 0
            self.counter[word][signature] += 1
            self.counter[word][self._sum_key] += 1

        self.ref_regex = re.compile(r"^([b-z]|([A-Z][A-Z]+))$")
        self.var_regex = re.compile(r"^[b-z]$")
        self.num_regex = re.compile(r"^\d+(\.\d+)?^")

    def get_log_distribution(self, word):
        dist = {}
        if word in self.counter:
            for sig, count in self.counter[word].iteritems():
                if sig == self._sum_key:
                    continue
                dist[sig] = np.log(float(count)/self.counter[word][self._sum_key])

        else:
            if self.num_regex.match(word):
                sig = FunctionSignature(word, "number", [])
                dist = {sig: 0.0}
            elif self.var_regex.match(word) and self.ref_regex.match(word):
                var_sig = FunctionSignature(word, "variable", [])
                ref_sig = FunctionSignature(word, "modifier", [])
                dist = {var_sig: np.log(0.5), ref_sig: np.log(0.5)}
            elif self.var_regex.match(word):
                sig = FunctionSignature(word, "variable", [])
                dist = {sig: 0.0}
            elif self.ref_regex.match(word):
                sig = FunctionSignature(word, "modifier", [])
                dist = {sig: 0.0}
            else:
                dist = {None: 0.0}

        return dist

