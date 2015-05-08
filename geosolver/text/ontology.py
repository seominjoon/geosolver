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
    return child == parent


types = ['root', 'start', 'number', 'modifier', 'circle', 'line', 'truth']
function_signatures = {}
tuples = (
    ('Root', 'root', ['start']),
    ('StartTruth', 'start', ['truth']),
    ('RadiusOf', 'number', ['circle']),
    ('IsRadius', 'truth', ['line', 'circle']),
    ('DiameterOf', 'number', ['circle']),
    ('IsDiameter', 'truth', ['line', 'circle']),
    ('IsChord', 'truth', ['line', 'circle']),
    ('IsMedian', 'truth', ['line', 'triangle']),
    ('IsAltitude', 'truth', ['line', 'triangle']),
    ('Equal', 'truth', ['number', 'number'], True),
    ('Circle', 'circle', ['modifier']),
    ('Line', 'line', ['modifier']),
    ('Triangle', 'triangle', ['modifier']),
    ('Angle', 'angle', ['modifier']),
    ('the', 'modifier', []),
    ('LengthOf', 'number', ['line']),
    ('Tangent', 'truth', ['line', 'circle']),
    ('Secant', 'truth', ['line', 'circle']),
    ('Perpendicular', 'truth', ['line', 'line']),
    ('Parallel', 'truth', ['line', 'line']),
    ('BisectsLine', 'truth', ['line', 'line']),
    ('BisectsAngle', 'truth', ['line', 'angle']),
    ('Find', 'truth', ['number']),
    #('Equivalent')
    ('Add', 'number', ['number', 'number']),
    ('circle', 'circle', []),
    ('unkNum', 'number', []),
    ('unkSt', 'truth', []),
    ('line', 'line', []),
    ('angle', 'angle', []),
)
for tuple_ in tuples:
    add_function_signature(function_signatures, tuple_)
