"""
For local running, including testing.
"""

from geosolver.ontology.augment_ontology import augment_ontology
from geosolver.ontology.ontology_proximity_score import ontology_proximity_score
from geosolver.utils import display_graph
from geosolver.ontology.states import Type, Function, BasicOntology
from geosolver.ontology import basic_ontology

__author__ = 'minjoon'


def test_load_ontology():
    o = basic_ontology
    print(o)
    print(o.inheritance_graph.edges())
    print(o.ontology_graph.edges(data=True))
    print(o.isinstance(o.types['triangle'], o.types['polygon']))


def test_symbol_proximity_score():
    o = basic_ontology
    # display_graph(o.inheritance_graph)
    # display_graph(o.ontology_graph)
    s0 = o.symbols['equal']
    s1 = o.symbols['line']
    score = ontology_proximity_score(o, s0, s1)
    print(score)


def test_augment_ontology():
    o = basic_ontology
    s0 = Function('5', [], o.types['number'])
    s1 = Function('O', [], o.types['reference'])
    oo = augment_ontology(o, [s0, s1])
    s2 = o.symbols['equal']
    s3 = o.symbols['radiusOf']
    s4 = o.symbols['isRadiusOf']
    s5 = o.symbols['circle']
    print(oo.function_proximity_score(s2, s5))

if __name__ == "__main__":
    # test_load_ontology()
    # test_symbol_proximity_score()
    test_augment_ontology()
