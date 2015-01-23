"""
For local running, including testing.
"""

from geosolver.ontology.augment_ontology import augment_ontology
from geosolver.ontology.get_ontology_graph_paths import get_ontology_graph_paths
from geosolver.ontology.ontology_proximity_score import ontology_proximity_score
from geosolver.ontology.states import Function
from geosolver.ontology import basic_ontology
from pprint import pprint

__author__ = 'minjoon'


def test_load_ontology():
    o = basic_ontology
    print(o.inheritance_graph.edges())
    print(o.ontology_graph.edges(data=True))
    print(o.isinstance(o.types['triangle'], o.types['polygon']))
    # o.display_ontology_graph()
    t = o.types['number']
    print(o.isinstance(t, t))



def test_function_proximity_score():
    o = basic_ontology
    # display_graph(o.inheritance_graph)
    # display_graph(o.ontology_graph)
    t0 = o.types['line']
    f1 = o.types['truth']
    score = ontology_proximity_score(o, t0, f1)
    print(score)



def test_augment_ontology():
    o = basic_ontology
    s0 = Function('5', [], o.types['number'])
    s1 = Function('O', [], o.types['reference'])
    oo = augment_ontology(o, {s0.name: s0, s1.name: s1})
    s2 = o.functions['equal']
    s3 = o.functions['radiusOf']
    s4 = o.functions['isRadiusOf']
    s5 = o.functions['circle']
    t0 = o.types['truth']
    pprint(get_ontology_graph_paths(oo, t0, s1))
    print(ontology_proximity_score(oo, t0, s1))

if __name__ == "__main__":
    # test_load_ontology()
    # test_function_proximity_score()
    test_augment_ontology()
