import networkx as nx

__author__ = 'minjoon'


class FunctionSignature(object):
    def __init__(self, id_, return_type, arg_types, arg_pluralities=None, is_symmetric=False, name=None):
        self.id = id_
        self.return_type = return_type
        self.arg_types = arg_types
        if name is None:
            name = id_
        self.name = name
        if arg_pluralities is None:
            arg_pluralities = (False,) * len(arg_types)
        self.arg_pluralities = arg_pluralities
        self.is_symmetric = is_symmetric
        self.valence = len(arg_types)

    def __repr__(self):
        return repr(self.name)

    def __eq__(self, other):
        assert isinstance(other, FunctionSignature)
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)


class Variable(object):
    def __init__(self, id_, return_type, name=None):
        self.id = id_
        self.return_type = return_type
        if name is None:
            name = id_
        self.name = name
        self.valence = 0

    def __repr__(self):
        return self.name


class Function(object):
    def __init__(self, signature, children):
        self.signature = signature
        for child in children:
            assert isinstance(child, Set)
        self.children = children

        self.return_type = signature.return_type


class Set(object):
    def __init__(self, head, members=None):
        self.head = head
        self.return_type = head.return_type
        if members is None:
            members = set([head])
        for member in members:
            assert isinstance(member, Function) or isinstance(member, Variable)
        self.members = members

    def is_singular(self):
        return len(self.members) == 1

    def is_plural(self):
        return len(self.members) > 1


class Span(tuple):
    def __new__(cls, start, end):
        obj = tuple.__new__(cls, (start, end))
        obj.is_single = start + 1 == end

    def __repr__(self):
        if self.is_single:
            return "%d" % self[0]
        else:
            return "%d:%d" % (self[0], self[1])


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