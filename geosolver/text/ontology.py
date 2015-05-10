from geosolver.text.ontology_states import FunctionSignature

__author__ = 'minjoon'

def add_function_signature(signatures, signature_tuple):
    if len(signature_tuple) == 3:
        name, return_type, arg_types = signature_tuple
        is_symmetric = False
    elif len(signature_tuple) == 4:
        name, return_type, arg_types, is_symmetric = signature_tuple
    assert name not in signatures
    signatures[name] = FunctionSignature(name, return_type, arg_types, is_symmetric)

def issubtype(child, parent):
    if child == 'variable' and parent == 'number':
        return True
    if child in ['triangle', 'quad'] and parent == 'polygon':
        return True
    if child in ['line', 'circle', 'triangle', 'quad'] and parent == 'entity':
        return True
    if child in ['circle', 'triangle', 'quad'] and parent == 'circle+polygon':
        return True
    return child == parent


types = ['root', 'start', 'number', 'modifier', 'circle', 'line', 'truth', 'point', 'quad', 'arc']
function_signatures = {}
tuples = (
    ('Root', 'root', ['start']),
    ('StartTruth', 'start', ['truth']),
    ('RadiusOf', 'number', ['circle']),
    ('IsRadius', 'truth', ['line', 'circle']),
    ('DiameterOf', 'number', ['circle']),
    ('IsDiameter', 'truth', ['line', 'circle']),
    ('IsSecant', 'truth', ['line', 'circle']),
    ('IsChord', 'truth', ['line', 'circle']),
    ('IsMedian', 'truth', ['line', 'triangle']),
    ('IsAltitude', 'truth', ['line', 'triangle']),
    ('Equal', 'truth', ['number', 'number'], True),
    ('Circle', 'circle', ['modifier']),
    ('Line', 'line', ['modifier']),
    ('Triangle', 'triangle', ['modifier']),
    ('Angle', 'angle', ['modifier']),
    ('AngleOfArc', 'number', ['arc']),
    ('Arc', 'arc', []),
    ('AngleOf', 'number', ['angle']),
    ('Point', 'point', ['modifier']),
    ('On', 'truth', ['point', 'line']),
    ('the', 'modifier', []),
    ('LengthOf', 'number', ['line']),
    ('Tangent', 'truth', ['line', 'circle']),
    ('Secant', 'truth', ['line', 'circle']),
    ('Perpendicular', 'truth', ['line', 'line'], True),
    ('Parallel', 'truth', ['line', 'line'], True),
    ('BisectsLine', 'truth', ['line', 'line']),
    ('BisectsAngle', 'truth', ['line', 'angle']),
    ('Find', 'truth', ['number']),
    #('Equivalent')
    # ('Add', 'number', ['number', 'number']),
    ('circle', 'circle', []),
    ('unkNum', 'number', []),
    ('unkSt', 'truth', []),
    ('line', 'line', []),
    ('angle', 'angle', []),
    ('quad', 'quad', []),
    ('all', 'modifier', []),
    ('IsRhombus', 'truth', ['quad']),
    ('Quad', 'quad', ['modifier']),
    ('PerimeterOf', 'number', ['polygon']),
    ('IsRight', 'truth', ['triangle']),
    ('IsHypotenuse', 'truth', ['line', 'triangle']),
    ('Intersects', 'truth', ['entity', 'entity'], True),
    ('IsMidpoint', 'truth', ['point', 'line']),
    ('Equilateral', 'truth', ['triangle']),
    ('Isosceles', 'truth', ['triangle']),
    ('AreaOf', 'number', ['circle+polygon']),
    ('IsSquare', 'truth', ['quad']),
    ('IsParallelogram', 'truth', ['quad']),
)
for tuple_ in tuples:
    add_function_signature(function_signatures, tuple_)
