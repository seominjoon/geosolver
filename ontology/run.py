"""
For local running, including testing.
"""

from geosolver.ontology import definitions
from geosolver.ontology.augment_ontology import augment_ontology
from geosolver.ontology.load_ontology import load_ontology
from geosolver.ontology.symbol_proximity_score import symbol_proximity_score
from geosolver.utils import display_graph
from geosolver.ontology.states import Type, Symbol, Ontology

__author__ = 'minjoon'


def test_load_ontology():
    o = load_ontology(definitions.types, definitions.symbols)
    print(o)
    print(o.inheritance_graph.edges())
    print(o.ontology_graph.edges(data=True))
    print(o.isinstance(o.types['triangle'], o.types['polygon']))


def test_symbol_proximity_score():
    o = load_ontology(definitions.types, definitions.symbols)
    # display_graph(o.inheritance_graph)
    # display_graph(o.ontology_graph)
    s0 = o.symbols['equal']
    s1 = o.symbols['line']
    score = symbol_proximity_score(o, s0, s1)
    print(score)


def test_augment_ontology():
    o = load_ontology(definitions.types, definitions.symbols)
    s0 = Symbol('5', '5', [], o.types['number'])
    s1 = Symbol('O', 'O', [], o.types['reference'])
    oo = augment_ontology(o, [s0, s1])
    s2 = o.symbols['equal']
    s3 = o.symbols['radius-number']
    s4 = o.symbols['radius-truth']
    s5 = o.symbols['circle']
    print(oo.symbol_proximity_score(s2, s5))

if __name__ == "__main__":
    # test_load_ontology()
    # test_symbol_proximity_score()
    test_augment_ontology()
