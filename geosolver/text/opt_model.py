import numpy as np

__author__ = 'minjoon'

class OptModel(object):
    @staticmethod
    def objective_function(semantic_trees):
        return 0.0


class TextGreedyOptModel(OptModel):
    def __init__(self, tag_rules):
        self.tag_rules = tag_rules

    def optimize(self, semantic_trees):
        selected = set()
        remaining = set(semantic_trees)
        next = TextGreedyOptModel.get_next(selected, remaining)
        curr_score = TextGreedyOptModel.objective_function(selected)
        next_score = TextGreedyOptModel.objective_function(selected.union([next]))
        while next_score - curr_score > 0:
            curr_score = next_score
            selected.add(next)
            remaining.discard(next)
            next = TextGreedyOptModel.get_next(selected, remaining)
            next_score = TextGreedyOptModel.objective_function(selected.union([next]))
        return selected

    @staticmethod
    def objective_function(semantic_trees):
        if len(semantic_trees) == 0:
            return 0.0

    @staticmethod
    def pairwise_redundancy(tree_a, tree_b):
        """
        First, return 0 if one of them is self-referencing unary tree
        Do not penalize leaf redundancies
        Penalize everything else

        :param tree_a:
        :param tree_b:
        :return:
        """
        a_spans = set(node.content.span for node in tree_a)
        b_spans = set(node.content.span for node in tree_b)
        common_spans = a_spans.intersection(b_spans)
        r = 0
        for span in common_spans:
            pass


    @staticmethod
    def get_next(selected, remaining):
        d = {each: TextGreedyOptModel.objective_function(selected.union([each])) for each in remaining}
        argmax = max(d.iteritems(), key=lambda pair: pair[1])[0]
        return argmax

