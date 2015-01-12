'''
Definitions of ontology
Contains types and symbols information.
The fields of a type is: name, label (optional), supertype (optional).
The fields of a symbol is: name,  arg_types, return_type, lemma (optional), label (optional)
If lemma is not specified, lemma will be set to name.
From these, an ontology object (states.Ontology) is constructed.
'''
import logging

__author__ = 'minjoon'

type_mandatory_keys = {'name'}
type_optional_keys = {'supertype', 'label'}
type_keys = type_mandatory_keys.union(type_optional_keys)

# note that 'lemma' is mandatory for Symbol; for convenience, at the end, lemma is copied from name
# if lemma is not present.
symbol_mandatory_keys = {'name', 'arg_types', 'return_type', 'lemma'}
symbol_optional_keys = ['label']
symbol_keys = symbol_mandatory_keys.union(symbol_optional_keys)

types = [
    # fundamental types
    {'name': 'number'},
    {'name': 'truth'},
    {'name': 'entity'},
    {'name': 'reference'},

    # subtypes
    {'name': 'point', 'supertype': 'entity'},
    {'name': 'line', 'supertype': 'entity'},
    {'name': 'arc', 'supertype': 'entity'},
    {'name': 'angle', 'supertype': 'entity'},
    {'name': 'polygon', 'supertype': 'entity'},
    {'name': 'circle', 'supertype': 'entity'},
    {'name': 'triangle', 'supertype': 'polygon'},
    {'name': 'quadrilateral', 'supertype': 'polygon'},
]

symbols = [
    # operators
    {'name': 'add', 'lemma': '+', 'arg_types': ['number', 'number'], 'return_type': 'number'},
    {'name': 'sub', 'lemma': '-', 'arg_types': ['number', 'number'], 'return_type': 'number'},
    {'name': 'mul', 'lemma': '*', 'arg_types': ['number', 'number'], 'return_type': 'number'},
    {'name': 'div', 'lemma': '/', 'arg_types': ['number', 'number'], 'return_type': 'number'},
    {'name': 'pow', 'lemma': '^', 'arg_types': ['number', 'number'], 'return_type': 'number'},

    # functions mapping to number
    {'name': 'length', 'arg_types': ['line'], 'return_type': 'number'},
    {'name': 'angle-number', 'lemma': 'angle', 'arg_types': ['angle'], 'return_type': 'number'},
    {'name': 'arc_angle', 'lemma': 'angle', 'arg_types': ['arc'], 'return_type': 'number'},
    {'name': 'radius-number', 'lemma': 'radius', 'arg_types': ['circle'], 'return_type': 'number'},
    {'name': 'diameter-number', 'lemma': 'diameter', 'arg_types': ['circle'], 'return_type': 'number'},
    {'name': 'polygon_area', 'lemma': 'area', 'arg_types': ['polygon'], 'return_type': 'number'},
    {'name': 'circle_area', 'lemma': 'area', 'arg_types': ['circle'], 'return_type': 'number'},
    {'name': 'perimeter', 'arg_types': ['polygon'], 'return_type': 'number'},
    {'name': 'circumference', 'arg_types': ['circle'], 'return_type': 'number'},

    # functions mapping to entities
    {'name': 'line', 'arg_types': ['reference'], 'return_type': 'line'},
    {'name': 'arc', 'arg_types': ['reference'], 'return_type': 'arc'},
    {'name': 'angle', 'arg_types': ['reference'], 'return_type': 'angle'},
    {'name': 'circle', 'arg_types': ['reference'], 'return_type': 'circle'},
    {'name': 'triangle', 'arg_types': ['reference'], 'return_type': 'triangle'},
    {'name': 'quadrilateral', 'arg_types': ['reference'], 'return_type': 'quadrilateral'},

    # functions mapping to truth value (predicates)
    {'name': 'exist', 'arg_types': ['entity'], 'return_type': 'truth'},
    {'name': 'intersect', 'arg_types': ['entity', 'entity'], 'return_type': 'truth'},
    {'name': 'on', 'arg_types': ['point', 'entity'], 'return_type': 'truth'},
    {'name': 'midpoint', 'arg_types': ['point', 'line'], 'return_type': 'truth'},
    {'name': 'parallel', 'arg_types': ['line', 'line'], 'return_type': 'truth'},
    {'name': 'perpendicular', 'arg_types': ['line', 'line'], 'return_type': 'truth'},
    {'name': 'line_bisect', 'lemma': 'bisect', 'arg_types': ['line', 'line'], 'return_type': 'truth'},
    {'name': 'angle_bisect', 'lemma': 'bisect', 'arg_types': ['line', 'angle'], 'return_type': 'truth'},
    {'name': 'angle_right', 'lemma': 'angle', 'arg_types': ['angle'], 'return_type': 'truth'},
    {'name': 'hypotenuse', 'arg_types': ['line', 'triangle'], 'return_type': 'truth'},
    {'name': 'median', 'arg_types': ['line', 'triangle'], 'return_type': 'truth'},
    {'name': 'altitude', 'arg_types': ['line', 'triangle'], 'return_type': 'truth'},
    {'name': 'isosceles', 'arg_types': ['triangle'], 'return_type': 'truth'},
    {'name': 'triangle_right', 'lemma': 'right', 'arg_types': ['triangle'], 'return_type': 'truth'},
    {'name': 'equilateral', 'arg_types': ['triangle'], 'return_type': 'truth'},
    {'name': 'parallelogram', 'arg_types': ['quadrilateral'], 'return_type': 'truth'},
    {'name': 'rhombus', 'arg_types': ['quadrilateral'], 'return_type': 'truth'},
    {'name': 'rectangle', 'arg_types': ['quadrilateral'], 'return_type': 'truth'},
    {'name': 'square', 'arg_types': ['quadrilateral'], 'return_type': 'truth'},
    {'name': 'radius-truth', 'lemma': 'radius', 'arg_types': ['line', 'circle'], 'return_type': 'truth'},
    {'name': 'diameter-truth', 'lemma': 'diameter', 'arg_types': ['line', 'circle'], 'return_type': 'truth'},
    {'name': 'chord', 'arg_types': ['line', 'circle'], 'return_type': 'truth'},
    {'name': 'tangent', 'arg_types': ['line', 'circle'], 'return_type': 'truth'},
    {'name': 'secant', 'arg_types': ['line', 'circle'], 'return_type': 'truth'},
]

# For each symbol, lemma is set to name if lemma is not given. Just for convenience.
for symbol in symbols:
    if 'lemma' not in symbol:
        symbol['lemma'] = symbol['name']


'''
Sanity check for definitions.py
Ensures several things:
1. each type/symbol has only valid keys, and all mandatory keys, and no duplicate definitions of keys
2. no two type/symbol has same name
3. supertype of each type is predefined in types
4. arg_types and return_type are defined in types
'''


def sanity_check():
    type_names = set()
    for idx, type_ in enumerate(types):
        keys = set()
        for key in type_:
            if key not in type_keys:
                logging.error("Invalid key encountered: '%s' at types:%d" % (key, idx))
                return False
            if key in keys:
                logging.error("Duplicate keys encountered: '%s' at types:%d" % (key, idx))
                return False
            keys.add(key)
        if not type_mandatory_keys.issubset(keys):
            missing_keys = type_mandatory_keys.difference(keys)
            logging.error("Some mandatory keys are missing: %r at types:%d" % (missing_keys, idx))
            return False
        if type_['name'] in type_names:
            logging.error("Non-unique name encountered: '%s' at types:%d" % (type_['name'], idx))
            return False
        if 'supertype' in type_ and type_['supertype'] not in type_names:
            logging.error("Unknown 'supertype': '%s' at type %r" % (type_['supertype'], type_))
        type_names.add(type_['name'])

    symbol_names = set()
    for idx, symbol_ in enumerate(symbols):
        keys = set()
        for key in symbol_:
            if key not in symbol_keys:
                logging.error("Invalid key encountered: '%s' at symbols:%d" % (key, idx))
                return False
            if key in keys:
                logging.error("Duplicate keys encountered: '%s' at symbols:%d" % (key, idx))
                return False
            keys.add(key)
        if not symbol_mandatory_keys.issubset(keys):
            missing_keys = symbol_mandatory_keys.difference(keys)
            logging.error("Some mandatory keys are missing: %r at symbol %r" % (list(missing_keys), symbol_))
            return False
        if symbol_['name'] in symbol_names:
            logging.error("Non-unique name encountered: '%s' at symbol %r" % (symbol_['name'], symbol_))
            return False
        for arg_type in symbol_['arg_types']:
            if arg_type not in type_names:
                logging.error("Unknown arg type: '%s' at symbol %r" % (arg_type, symbol_))
                return False
        if symbol_['return_type'] not in type_names:
            logging.error("Unknown return type: '%s' at symbol %r" % (symbol_['return_type'], symbol_))
            return False

        symbol_names.add(symbol_['name'])

    # passed every test
    return True

if not sanity_check():
    raise Exception("Ontology definitions are invalid.")
logging.info("Ontology definitions verified.")
