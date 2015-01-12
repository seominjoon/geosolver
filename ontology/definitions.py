"""
Definitions of ontology
Contains types and symbols information.
The fields of a type is: name, label (optional), supertype (optional).
The fields of a symbol is: name,  arg_types, return_type, lemma (optional), label (optional)
If lemma is not specified, lemma will be set to name.
From these, an ontology object (states.Ontology) is constructed.
"""

__author__ = 'minjoon'


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
