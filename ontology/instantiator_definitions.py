"""
Semantic definitions of ontology.

All functions need to be defined in terms of sympy's symbolic representations.
See ontology/basic_definitions.py for ontology.
If the function needs to return a truth value, then it must return an instance of 'Truth'.
Otherwise, it returns a sympy expression (can be a constant).
"""
from collections import namedtuple

__author__ = 'minjoon'


instantiator_defs = {
    'point': (('x', 'number'), ('y', 'number')),
    'line': (('a', 'point'), ('b', 'point')),
    'angle': (('a', 'point'), ('b', 'point'), ('c', 'point')),
    'circle': (('center', 'point'), ('radius', 'number')),
    'arc': (('circle', 'circle'), ('a', 'point'), ('b', 'point')),
    'triangle': (('a', 'point'), ('b', 'point'), ('c', 'point')),
    'quadrilateral': (('a', 'point'), ('b', 'point'), ('c', 'point'), ('d', 'point')),
}



"""
Initialize instantiators based on type_defs
"""
instantiators = {}
for key, value in instantiator_defs.iteritems():
    args, _ = zip(*value)
    nt = namedtuple(key, ' '.join(args))
    instantiators[key] = nt


def polygon(*args):
    if len(args) == 3:
        return instantiators['triangle'](*args)
    elif len(args) == 4:
        return instantiators['quadrilateral'](*args)
    else:
        raise Exception()

# instantiators['polygon'] = polygon
