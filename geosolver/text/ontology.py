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
    return child == parent


types = ['root', 'start', 'number', 'modifier', 'circle', 'line', 'truth']
function_signatures = {}
tuples = (
    ('Root', 'root', ['start']),
    ('StartTruth', 'start', ['truth']),
    ('RadiusOf', 'number', ['circle']),
    ('isRadiusOf', 'truth', ['line', 'circle']),
    ('Equal', 'truth', ['number', 'number'], True),
    ('Circle', 'circle', ['modifier']),
    ('Line', 'line', ['modifier']),
    ('The', 'modifier', []),
    ('Length', 'number', ['line']),
    ('Tangent', 'truth', ['line', 'circle']),
    ('Secant', 'truth', ['line', 'circle']),
    #('Add', 'number', ['number', 'number']),
    ('circle', 'circle', []),
    ('unkNum', 'number', []),
    ('unkSt', 'truth', []),
    ('line', 'line', []),
)
for tuple_ in tuples:
    add_function_signature(function_signatures, tuple_)
