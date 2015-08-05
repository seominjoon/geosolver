from geosolver.text.rule import UnaryRule, BinaryRule

__author__ = 'minjoon'

class FeatureFunction(object):
    def map(self, rule):
        pass


class UnaryFeatureFunction(FeatureFunction):
    def __init__(self, unary_rules):
        self.nbr_rel_set = set()
        self.mid_tag_set = set()
        self.graph_dist_set = {0, 1, 2}
        self.plain_dist_set = {1, 2}
        self.p_tag_set = set()
        self.c_tag_set = set()
        self.p_return_type_set = set()
        self.c_return_type_set = set()

        for unary_rule in unary_rules:
            assert isinstance(unary_rule, UnaryRule)
            sp, p, c = unary_rule.syntax_parse, unary_rule.parent_tag_rule, unary_rule.child_tag_rule
            graph_distance = sp.distance_between_spans(p.span, c.span)
            if graph_distance == 1:
                rel = sp.relation_between_spans(p.span, c.span)
                self.nbr_rel_set.add(rel)
            elif graph_distance == 2:
                path = sp.shortest_path_between_spans(p.span, c.span)
                assert len(path) == 3
                mid_tag = sp.get_tag_by_index(path[1])
                self.mid_tag_set.add(mid_tag)

            self.p_tag_set.add(sp.get_tag_by_span(p.span))
            self.c_tag_set.add(sp.get_tag_by_span(c.span))
            self.p_return_type_set.add(p.signature.return_type)
            self.c_return_type_set.add(c.signature.return_type)


    def map(self, ur):
        assert isinstance(ur, UnaryRule)
        out = []
        sp, p, c = ur.syntax_parse, ur.parent_tag_rule, ur.child_tag_rule
        d = sp.distance_between_spans(p.span, c.span)
        pd = sp.plain_distance_between_spans(p.span, c.span, True)

        for ref_d in self.graph_dist_set:
            out.append(int(d == ref_d))
        for ref_pd in self.plain_dist_set:
            out.append(int(abs(pd) == ref_pd))
        for ref_rel in self.nbr_rel_set:
            out.append(int(d == 1 and ref_rel == sp.relation_between_spans(p.span, c.span)))
        for ref_tag in self.mid_tag_set:
            out.append(int(d == 2 and ref_tag == sp.get_tag_by_index(sp.shortest_path_between_spans(p.span, c.span)[1])))
        out.append(int(pd >= 0))

        for ref_p_tag in self.p_tag_set:
            out.append(int(ref_p_tag == sp.get_tag_by_span(p.span)))
        for ref_c_tag in self.c_tag_set:
            out.append(int(ref_c_tag == sp.get_tag_by_span(c.span)))
        for ref_p_return_type in self.p_return_type_set:
            out.append(int(ref_p_return_type == p.signature.return_type))
        for ref_c_return_type in self.p_return_type_set:
            out.append(int(ref_c_return_type == p.signature.return_type))

        return tuple(out)


def binary_rule_to_unary_rules(binary_rule):
    assert isinstance(binary_rule, BinaryRule)
    p, a, b = binary_rule.parent_tag_rule, binary_rule.child_a_tag_rule, binary_rule.child_b_tag_rule
    pa = UnaryRule(p, a)
    pb = UnaryRule(p, b)
    ab = UnaryRule(a, b)
    return pa, pb, ab


class BinaryFeatureFunction(FeatureFunction):
    def __init__(self, binary_rules):
        pas, pbs, abs = zip(*[binary_rule_to_unary_rules(br) for br in binary_rules])
        self.pa_ff = UnaryFeatureFunction(pas)
        self.pb_ff = UnaryFeatureFunction(pbs)
        self.ab_ff = UnaryFeatureFunction(abs)

    def map(self, rule):
        pa, pb, ab = binary_rule_to_unary_rules(rule)
        pa_fv = self.pa_ff.map(pa)
        pb_fv = self.pa_ff.map(pb)
        ab_fv = self.pa_ff.map(ab)
        fv = pa_fv + pb_fv + ab_fv
        return fv
