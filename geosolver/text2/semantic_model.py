__author__ = 'minjoon'

class SemanticModel(object):
    def __init__(self, tag_model, feature_function, weights=None):
        self.tag_model = tag_model
        self.feature_function = feature_function
        self.weights = weights

    def fit(self, semantic_rules):
        pass

    def get_all_rules(self, syntax_parse):
        pass

    def get_log_prob(self, syntax_parse, semantic_rule):
        pass


class LogLinearSemanticModel(SemanticModel):
    pass

class UnaryLogLinearSemanticModel(LogLinearSemanticModel):
    pass