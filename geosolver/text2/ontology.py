import networkx as nx

__author__ = 'minjoon'


class Signature(object):
    def __init__(self, id_, return_type, valence, name=None):
        self.id = id_
        self.return_type = return_type
        if name is None:
            if isinstance(id_, str):
                name = id_
            else:
                name = repr(id_)
        self.name = name
        self.valence = valence

    def __eq__(self, other):
        assert isinstance(other, Signature)
        return self.id == other.id

class FunctionSignature(Signature):
    def __init__(self, id_, return_type, arg_types, arg_pluralities=None, is_symmetric=False, name=None):
        super(FunctionSignature, self).__init__(id_, return_type, len(arg_types), name=name)
        self.arg_types = arg_types
        if arg_pluralities is None:
            arg_pluralities = (False,) * len(arg_types)
        self.arg_pluralities = arg_pluralities
        self.is_symmetric = is_symmetric
        self.valence = len(arg_types)

    def __repr__(self):
        return self.name


    def __hash__(self):
        return hash(self.id)


class VariableSignature(Signature):
    def __init__(self, id_, return_type, name=None):
        super(VariableSignature, self).__init__(id_, return_type, 0, name=name)

    def __repr__(self):
        return self.name


class FunctionNode(object):
    def __init__(self, signature, children):
        self.signature = signature
        for child in children:
            assert isinstance(child, SetNode)
        self.children = children

        self.return_type = signature.return_type


class SetNode(object):
    def __init__(self, head, members=None):
        self.head = head
        self.return_type = head.return_type
        if members is None:
            members = set([head])
        for member in members:
            assert isinstance(member, FunctionNode) or isinstance(member, VariableSignature)
        self.members = members

    def is_singular(self):
        return len(self.members) == 1

    def is_plural(self):
        return len(self.members) > 1


types = ('root', 'truth', 'number', 'entity', 'line', 'circle', 'triangle', 'quad', 'polygon')
type_inheritances = (
    ('root', 'truth'),
    ('root', 'number'),
    ('root', 'entity'),
    ('entity', 'point'),
    ('entity', '1d'),
    ('1d', 'line'),
    ('1d', 'angle'),
    ('1d', 'arc'),
    ('entity', '2d'),
    ('2d', 'polygon'),
    ('2d', 'circle'),
    ('polygon', 'triangle'),
    ('polygon', 'quad'),
    ('polygon', 'hexagon'),

)
type_graph = nx.DiGraph()
for parent, child in type_inheritances:
    type_graph.add_edge(parent, child)


def issubtype(child_type, parent_type):
    return nx.has_path(type_graph, parent_type, child_type)

function_signature_tuples = (
    ('IsLine', 'truth', ['line']),
    ('IntersectionOf', 'point', ['entity', 'entity'], None, True),
    ('Is', 'truth', ['root', 'root'], None, True),
    ('Equals', 'truth', ['number', 'number']),
    ('What', 'number', []),
    ('ValueOf', 'number', ['number']),
    ('IsTriangle', 'truth', ['triangle']),
    ('InscribedIn', 'truth', ['polygon', 'circle']),
    ('IsCenterOf', 'truth', ['point', '2d']),
    ('IsDiameterLineOf', 'truth', ['line', 'circle']),
    ('DegreeMeasureOf', 'number', ['angle']),
    ('IsAngle', 'truth', ['angle']),
    ('Equilateral', 'truth', ['triangle']),
    ('IsSquare', 'truth', ['quad']),
    ('AreaOf', 'number', ['2d']),
    ('PerimeterOf', 'number', ['polygon']),
    ('IsMidpointOf', 'truth', ['point', 'line']),
    ('LengthOf', 'number', ['line']),
    ('Conj', 'truth', ['root', 'root'], None, True),
)

def get_function_signatures():
    local_function_signatures = {}
    for tuple_ in function_signature_tuples:
        if len(tuple_) == 3:
            id_, return_type, arg_types = tuple_
            function_signature = FunctionSignature(id_, return_type, arg_types)
        elif len(tuple_) == 5:
            id_, return_type, arg_types, arg_pluralities, is_symmetric = tuple_
            function_signature = FunctionSignature(id_, return_type, arg_types, arg_pluralities, is_symmetric)
        local_function_signatures[id_] = function_signature
    return local_function_signatures

function_signatures = get_function_signatures()