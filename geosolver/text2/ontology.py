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
        self.children = children
        self.return_type = signature.return_type

    def is_leaf(self):
        return len(self.children) == 0


    def __add__(self, other):
        current = function_signatures['Add']
        return FunctionNode(current, [self, other])

    def __radd__(self, other):
        current = function_signatures['Add']
        return FunctionNode(current, [other, self])

    def __mul__(self, other):
        current = function_signatures['Mul']
        return FunctionNode(current, [self, other])

    def __rmul__(self, other):
        current = function_signatures['Mul']
        return FunctionNode(current, [other, self])

    def __sub__(self, other):
        current = function_signatures['Sub']
        return FunctionNode(current, [self, other])

    def __rsub__(self, other):
        current = function_signatures['Sub']
        return FunctionNode(current, [other, self])

    def __div__(self, other):
        current = function_signatures['Div']
        return FunctionNode(current, [self, other])

    def __rdiv__(self, other):
        current = function_signatures['Div']
        return FunctionNode(current, [other, self])

    def __pow__(self, power, modulo=None):
        current = function_signatures['Pow']
        return FunctionNode(current, [self, power])

    def __rpow__(self, power, modulo=None):
        current = function_signatures['Pow']
        return FunctionNode(current, [power, self])

    def __eq__(self, other):
        current = function_signatures['Equals']
        return FunctionNode(current, [self, other])

    def __ge__(self, other):
        current = function_signatures['Ge']
        return FunctionNode(current, [self, other])

    def __lt__(self, other):
        current = function_signatures['Lt']
        return FunctionNode(current, [self, other])

    def __repr__(self):
        if self.is_leaf():
            return repr(self.signature)
        else:
            return "%r(%s)" % (self.signature, ",".join(repr(child) for child in self.children))


class SetNode(object):
    def __init__(self, head, members=None):
        self.head = head
        self.return_type = head.return_type
        if members is None:
            members = set([head])
        for member in members:
            assert isinstance(member, FunctionNode)
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
    ('Point', 'point', ['number', 'number']),
    ('Line', 'line', ['point', 'point'], None, True),
    ('Circle', 'line', ['point', 'number']),
    ('Angle', 'angle', ['point', 'point', 'point']),
    ('Arc', 'arc', ['circle', 'point', 'point']),
    ('IntersectionOf', 'point', ['entity', 'entity'], None, True),
    ('Is', 'truth', ['root', 'root'], None, True),
    ('Equals', 'truth', ['number', 'number']),
    ('Add', 'number', ['number', 'number'], None, True),
    ('Mul', 'number', ['number', 'number'], None, True),
    ('Sub', 'number', ['number', 'number']),
    ('Div', 'number', ['number', 'number']),
    ('Pow', 'number', ['number', 'number']),
    ('Ge', 'truth', ['number', 'number']),
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
    ('Same', 'truth', ['entity', 'entity'], None, True),
    ('MeasureOf', 'number', ['angle']),
    ('Perpendicular', 'truth', ['line', 'line'], None, True),
    ('IsChordOf', 'truth', ['line', 'circle']),
    ('Tangent', 'truth', ['line', 'circle']),
    ('RadiusOf', 'number', ['circle']),
    ('PointLiesOnLine', 'truth', ['point', 'line']),
    ('PointLiesOnCircle', 'truth', ['point', 'circle']),
    ('Sqrt', 'number', ['number']),
    ('Parallel', 'truth', ['line', 'line'], None, True),
)

abbreviations = {
    '+': 'Add',
    '-': 'Sub',
    '*': 'Mul',
    '/': 'Div',
    ':': 'Div',
    '=': 'Equals',
    '<': 'Ge',
    '^': 'Pow',
    '\\sqrt': 'Sqrt',
    '||': 'Parallel',
}

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