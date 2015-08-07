import numpy as np
from geosolver.text.rule import UnaryRule
from geosolver.text.rule_model import CombinedModel
from geosolver.text.semantic_tree import SemanticTreeNode

__author__ = 'minjoon'

class GreedyOptModel(object):
    def __init__(self, combined_model):
        assert isinstance(combined_model, CombinedModel)
        self.combined_model = combined_model

    def objective_function(self, semantic_trees):
        return 0.0

    def optimize(self, semantic_trees, threshold):
        return set()

class TextGreedyOptModel(GreedyOptModel):
    def optimize(self, semantic_trees, threshold):
        selected = set()
        remaining = set(semantic_trees)

        curr_score = self.objective_function(selected)
        next_tree, next_score = self.get_next_tree(selected, remaining)
        if next_tree is None:
            print "No legal next available."
            return set()
        while next_score - curr_score > threshold:
            print "%.3f, %r" % (next_score, next_tree)
            curr_score = next_score
            selected.add(next_tree)
            remaining.discard(next_tree)
            next_tree, next_score = self.get_next_tree(selected, remaining)
            if next_tree is None:
                print "No legal next available."
                break
            next_score = self.objective_function(selected.union([next_tree]))
            if len(selected) > 30:
                raise Exception()
        return selected

    def objective_function(self, semantic_trees):
        if len(semantic_trees) == 0:
            return 0.0
        sum_log = sum(np.log(self.combined_model.get_tree_score(tree)) for tree in semantic_trees)
        cov = len(set(tr.span for semantic_tree in semantic_trees for tr in semantic_tree.get_tag_rules()))
        return cov + sum_log

    @staticmethod
    def pairwise_legal(a_tree, b_tree):
        """
        First, return 0 if one of them is self-referencing unary tree
        Do not penalize leaf redundancies
        Penalize everything else

        :param a_tree:
        :param b_tree:
        :return:
        """
        assert isinstance(a_tree, SemanticTreeNode)
        assert isinstance(b_tree, SemanticTreeNode)
        a_spans = set(node.content.span for node in a_tree)
        b_spans = set(node.content.span for node in b_tree)
        common_spans = a_spans.intersection(b_spans)
        for span in common_spans:
            a_tags = a_tree.get_tag_rules_by_span(span)
            b_tags = b_tree.get_tag_rules_by_span(span)
            if a_tags != b_tags:
                return False
        return True


    def get_next_tree(self, selected, remaining):
        d = {each: self.objective_function(selected.union([each])) for each in remaining
             if all(TextGreedyOptModel.pairwise_legal(each, each_selected) for each_selected in selected)}
        if len(d) == 0:
            return None, None
        pair = max(d.iteritems(), key=lambda pair: pair[1])
        return pair

