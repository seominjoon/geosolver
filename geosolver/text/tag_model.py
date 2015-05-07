import itertools
import numpy as np
import re
from geosolver.text.ontology import function_signatures
from geosolver.text.ontology_states import FunctionSignature

__author__ = 'minjoon'

class TagModel(object):
    def __init__(self):
        pass

    def get_log_distribution(self, words, syntax_tree, index):
        """
        TO BE OVERRIDDEN

        :param words:
        :param syntax_tree:
        :param index:
        :return:
        """
        pass

    def get_best_tag(self, words, syntax_tree, index):
        dist = self.get_log_distribution(words, syntax_tree, index)
        return max(dist.items(), key=lambda x: x[1])

    def get_best_tags(self, words, syntax_tree):
        tags = {index: self.get_best_tag(words, syntax_tree, index)[0] for index in words.keys()}
        return tags

    def get_log_combinations(self, words, syntax_tree):
        combinations = []
        indices = words.keys()
        distributions = [self.get_log_distribution(words, syntax_tree, index) for index in indices]
        for pairs in itertools.product(*distributions):
            tags = {indices[index]: pair[0] for index, pair in enumerate(pairs) if pair[0] is not None}
            prob = sum(pair[1] for pair in pairs if pair[0] is not None)
            combinations.append((tags, prob))
        return combinations


class RuleBasedTagModel(TagModel):
    def get_log_distribution(self, words, syntax_tree, index):
        """
        Returns a dictionary of signature:probability pair
        :param words:
        :param syntax_tree:
        :param index:
        :return:
        """
        if words[index] == 'radius':
            return {function_signatures['RadiusOf']: 0.0}
        elif words[index] == 'circle':
            return {function_signatures['Circle']: 0.0}
        elif words[index] == 'O':
            return {FunctionSignature('O', 'modifier', []): 0.0}
        elif words[index] == '5':
            return {FunctionSignature('5', 'number', []): 0.0}
        elif words[index] == 'the':
            return {function_signatures['The']: np.log(0.05), None: np.log(0.95)}
        elif words[index] == 'line':
            return {function_signatures['Line']: 0.0}
        else:
            return {None: 0.0}


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

    def get_log_distribution(self, words, syntax_tree, index):
        word = words[index]
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

