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
    {'name': 'add', 'arg_types': ['number', 'number'], 'return_type': 'number'},
    {'name': 'sub', 'arg_types': ['number', 'number'], 'return_type': 'number'},
    {'name': 'mul', 'arg_types': ['number', 'number'], 'return_type': 'number'},
    {'name': 'div', 'arg_types': ['number', 'number'], 'return_type': 'number'},
    {'name': 'pow', 'arg_types': ['number', 'number'], 'return_type': 'number'},
    {'name': 'equal', 'arg_types': ['number', 'number'], 'return_type': 'number'},
    {'name': 'greater', 'arg_types': ['number', 'number'], 'return_type': 'number'},
    {'name': 'less', 'arg_types': ['number', 'number'], 'return_type': 'number'},

    # functions mapping to number
    {'name': 'lengthOf', 'arg_types': ['line'], 'return_type': 'number'},
    {'name': 'angleOf:angle', 'arg_types': ['angle'], 'return_type': 'number'},
    {'name': 'angleOf:arc', 'arg_types': ['arc'], 'return_type': 'number'},
    {'name': 'radiusOf', 'arg_types': ['circle'], 'return_type': 'number'},
    {'name': 'diameterOf', 'arg_types': ['circle'], 'return_type': 'number'},
    {'name': 'areaOf:polygon', 'arg_types': ['polygon'], 'return_type': 'number'},
    {'name': 'areaOf:circle', 'arg_types': ['circle'], 'return_type': 'number'},
    {'name': 'perimeterOf', 'arg_types': ['polygon'], 'return_type': 'number'},
    {'name': 'circumferenceOf', 'arg_types': ['circle'], 'return_type': 'number'},

    # functions mapping to entities
    {'name': 'line', 'arg_types': ['reference'], 'return_type': 'line'},
    {'name': 'arc', 'arg_types': ['reference'], 'return_type': 'arc'},
    {'name': 'angle', 'arg_types': ['reference'], 'return_type': 'angle'},
    {'name': 'circle', 'arg_types': ['reference'], 'return_type': 'circle'},
    {'name': 'triangle', 'arg_types': ['reference'], 'return_type': 'triangle'},
    {'name': 'quadrilateral', 'arg_types': ['reference'], 'return_type': 'quadrilateral'},

    # functions mapping to truth value (predicates)
    {'name': 'exists', 'arg_types': ['entity'], 'return_type': 'truth'},
    {'name': 'intersects', 'arg_types': ['entity', 'entity'], 'return_type': 'truth'},
    {'name': 'isOn', 'arg_types': ['point', 'entity'], 'return_type': 'truth'},
    {'name': 'isMidpointOf', 'arg_types': ['point', 'line'], 'return_type': 'truth'},
    {'name': 'isParallelWith', 'arg_types': ['line', 'line'], 'return_type': 'truth'},
    {'name': 'isPerpendicularTo', 'arg_types': ['line', 'line'], 'return_type': 'truth'},
    {'name': 'bisects:line', 'arg_types': ['line', 'line'], 'return_type': 'truth'},
    {'name': 'bisects:angle', 'arg_types': ['line', 'angle'], 'return_type': 'truth'},
    {'name': 'isRightAngle', 'arg_types': ['angle'], 'return_type': 'truth'},
    {'name': 'isHypotenuseOf', 'arg_types': ['line', 'triangle'], 'return_type': 'truth'},
    {'name': 'isMedianOf', 'arg_types': ['line', 'triangle'], 'return_type': 'truth'},
    {'name': 'isAltitudeOf', 'arg_types': ['line', 'triangle'], 'return_type': 'truth'},
    {'name': 'isIsosceles', 'arg_types': ['triangle'], 'return_type': 'truth'},
    {'name': 'isRightTriangle', 'arg_types': ['triangle'], 'return_type': 'truth'},
    {'name': 'isEquilateral', 'arg_types': ['triangle'], 'return_type': 'truth'},
    {'name': 'isParallelogram', 'arg_types': ['quadrilateral'], 'return_type': 'truth'},
    {'name': 'isRhombus', 'arg_types': ['quadrilateral'], 'return_type': 'truth'},
    {'name': 'isRectangle', 'arg_types': ['quadrilateral'], 'return_type': 'truth'},
    {'name': 'isSquare', 'arg_types': ['quadrilateral'], 'return_type': 'truth'},
    {'name': 'isRadiusOf', 'arg_types': ['line', 'circle'], 'return_type': 'truth'},
    {'name': 'isDiameterOf', 'arg_types': ['line', 'circle'], 'return_type': 'truth'},
    {'name': 'isChordOf', 'arg_types': ['line', 'circle'], 'return_type': 'truth'},
    {'name': 'isTangentOf', 'arg_types': ['line', 'circle'], 'return_type': 'truth'},
    {'name': 'isSecantOf', 'arg_types': ['line', 'circle'], 'return_type': 'truth'},
]
