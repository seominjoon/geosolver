import itertools
import networkx as nx
from geosolver.utils.num import is_number

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

    def __hash__(self):
        return hash(self.id)

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



class VariableSignature(Signature):
    def __init__(self, id_, return_type, name=None):
        super(VariableSignature, self).__init__(id_, return_type, 0, name=name)

    def __repr__(self):
        return "$%s:%s" % (self.name, self.return_type)

    def is_ref(self):
        """
        starts with '@'
        :return:
        """
        if isinstance(self.name, str):
            return self.name.startswith("@")
        return False


class Node(object):
    def __init__(self, children, parent=None, index=None):
        self.parent = parent
        self.index = index
        self.children = children
        for idx, child in enumerate(children):
            if isinstance(child, Node):
                child.parent = self
                child.index = idx

    def is_leaf(self):
        return len(self.children) == 0

    def replace_node(self, tester, getter=None):
        args = [child.replace_node(tester, getter) for child in self.children]
        out = self.__class__(args, self.parent, self.index)
        test = tester(out)
        if bool(test):
            if getter is None:
                return test
            return getter(out)
        return out

    def __iter__(self):
        yield self
        for x in itertools.chain(*[iter(child) for child in self.children]):
            yield x

    def is_singular(self):
        return len(self.children) == 1

    def is_plural(self):
        return len(self.children) > 1

    def has_signature(self, id_):
        return any(not is_number(child) and child.has_signature(id_) for child in self.children)

    def is_grounded(self, ids=[]):
        return all(child.is_grounded(ids) for child in self.children)

    def get_nodes(self, tester):
        out = []
        for node in self:
            if tester(node):
                out.append(node)
        return out




class FormulaNode(Node):
    def __init__(self, signature, children, parent=None, index=None):
        self.signature = signature
        super(FormulaNode, self).__init__(children, parent, index)
        self.return_type = signature.return_type


    def replace_signature(self, tester, getter):
        """
        iterate through all formula nodes and if tester(signature) is true,
         then replace_signature it with getter(signature).
        :param function tester:
        :param function getter:
        :return:
        """
        new_sig = self.signature
        args = [child.replace_signature(tester, getter) for child in self.children]
        if tester(self.signature):
            new_sig = getter(self.signature)
        return FormulaNode(new_sig, args)

    def replace_node(self, tester, getter=None):
        args = []
        for child in self.children:
            if isinstance(child, Node):
                args.append(child.replace_node(tester, getter))
            else:
                args.append(child)
        out = self.__class__(self.signature, args, self.parent, self.index)
        test = tester(out)
        if bool(test):
            if getter is None:
                return test
            return getter(out)
        return out


    def __add__(self, other):
        current = signatures['Add']
        return FormulaNode(current, [self, other])

    def __radd__(self, other):
        current = signatures['Add']
        return FormulaNode(current, [other, self])

    def __mul__(self, other):
        current = signatures['Mul']
        return FormulaNode(current, [self, other])

    def __rmul__(self, other):
        current = signatures['Mul']
        return FormulaNode(current, [other, self])

    def __sub__(self, other):
        current = signatures['Sub']
        return FormulaNode(current, [self, other])

    def __rsub__(self, other):
        current = signatures['Sub']
        return FormulaNode(current, [other, self])

    def __div__(self, other):
        current = signatures['Div']
        return FormulaNode(current, [self, other])

    def __rdiv__(self, other):
        current = signatures['Div']
        return FormulaNode(current, [other, self])

    def __pow__(self, power, modulo=None):
        current = signatures['Pow']
        return FormulaNode(current, [self, power])

    def __rpow__(self, power, modulo=None):
        current = signatures['Pow']
        return FormulaNode(current, [power, self])

    def __eq__(self, other):
        current = signatures['Equals']
        return FormulaNode(current, [self, other])

    def __ge__(self, other):
        current = signatures['Ge']
        return FormulaNode(current, [self, other])

    def __lt__(self, other):
        current = signatures['Lt']
        return FormulaNode(current, [self, other])

    def __repr__(self):
        if isinstance(self.signature, VariableSignature):
            return repr(self.signature)
        return "%r(%s)" % (self.signature, ",".join(repr(child) for child in self.children))

    def has_signature(self, id_):
        if self.signature.id == id_:
            return True
        return any(not is_number(child) and child.has_signature(id_) for child in self.children)

    def is_grounded(self, ids=[]):
        """
        Determines if the formula's variables are only made of ids
        :param core_parse:
        :return:
        """
        if self.is_leaf():
            if isinstance(self.signature, VariableSignature):
                return self.signature.id in ids
            return True
        return all(not isinstance(child, Node) or child.is_grounded(ids) for child in self.children)


class SetNode(Node):
    def __init__(self, children, parent=None, index=None, head_index=0):
        super(SetNode, self).__init__(children, parent, index)
        self.head = children[head_index]

    def __repr__(self):
        return "{%s}" % ",".join(repr(child) for child in self.children)


type_inheritances = (
    ('root', 'truth'),
    ('root', 'number'),
    ('root', 'entity'),
    ('entity', 'point'),
    ('entity', 'oned'),
    ('oned', 'line'),
    ('oned', 'angle'),
    ('oned', 'arc'),
    ('entity', 'twod'),
    ('twod', 'polygon'),
    ('twod', 'circle'),
    ('polygon', 'triangle'),
    ('polygon', 'quad'),
    ('polygon', 'hexagon'),
)

types = set().union(*[set(inheritance) for inheritance in type_inheritances])

type_graph = nx.DiGraph()
for parent, child in type_inheritances:
    type_graph.add_edge(parent, child)


def issubtype(child_type, parent_type):
    return nx.has_path(type_graph, parent_type, child_type)

def is_singular(type_):
    return type_ in types

def is_plural(type_):
    return type_[:-1] in types and type_[-1] == 's'

function_signature_tuples = (
    ('Not', 'truth', ['truth']),
    ('True', 'truth', ['truth']),
    ('IsLine', 'truth', ['line']),
    ('IsPoint', 'truth', ['point']),
    ('IsCircle', 'truth', ['circle']),
    ('IsTriangle', 'truth', ['triangle']),
    ('IsQuad', 'truth', ['quad']),
    ('IsRectangle', 'truth', ['quad']),
    ('IsTrapezoid', 'truth', ['quad']),
    ('IsPolygon', 'truth', ['polygon']),
    ('IsRegular', 'truth', ['polygon']),
    ('Point', 'point', ['number', 'number']),
    ('Line', 'line', ['point', 'point'], None, True),
    ('Arc', 'arc', ['circle', 'point', 'point']),
    ('Circle', 'line', ['point', 'number']),
    ('Angle', 'angle', ['point', 'point', 'point']),
    ('Triangle', 'triangle', ['point', 'point', 'point']),
    ('Quad', 'quad', ['point', 'point', 'point', 'point']),
    ('Arc', 'arc', ['circle', 'point', 'point']),
    ('Polygon', 'polygon', ['*point']),
    ('Hexagon', 'hexagon', ['point', 'point', 'point', 'point', 'point', 'point']),
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
    ('IsInscribedIn', 'truth', ['polygon', 'circle']),
    ('IsCenterOf', 'truth', ['point', 'twod']),
    ('IsDiameterLineOf', 'truth', ['line', 'circle']),
    ('DegreeMeasureOf', 'number', ['angle']),
    ('IsAngle', 'truth', ['angle']),
    ('Equilateral', 'truth', ['triangle']),
    ('Isosceles', 'truth', ['triangle']),
    ('IsSquare', 'truth', ['quad']),
    ('IsRight', 'truth', ['triangle']),
    ('AreaOf', 'number', ['twod']),
    ('IsAreaOf', 'truth', ['number', 'twod']),
    ('IsLengthOf', 'truth', ['number', 'line']),
    ('IsRectLengthOf', 'truth', ['number', 'quad']),
    ('IsDiameterNumOf', 'truth', ['number', 'circle']),
    ('IsSideOf', 'truth', ['number', 'quad']),
    ('PerimeterOf', 'number', ['polygon']),
    ('IsMidpointOf', 'truth', ['point', 'line']),
    ('IsWidthOf', 'truth', ['number', 'quad']),
    ('LengthOf', 'number', ['line']),
    ('CC', 'truth', ['root', 'root'], None, True),
    ('Is', 'truth', ['entity', 'entity'], None, True),
    ('MeasureOf', 'number', ['angle']),
    ('Perpendicular', 'truth', ['line', 'line'], None, True),
    ('IsChordOf', 'truth', ['line', 'circle']),
    ('Tangent', 'truth', ['line', 'twod']),
    ('RadiusOf', 'number', ['circle']),
    ('IsRadiusNumOf', 'truth', ['number', 'circle']),
    ('IsRadiusLineOf', 'truth', ['line', 'circle']),
    ('PointLiesOnLine', 'truth', ['point', 'line']),
    ('PointLiesOnCircle', 'truth', ['point', 'circle']),
    ('Sqrt', 'number', ['number']),
    ('Parallel', 'truth', ['line', 'line'], None, True),
    ('IntersectAt', 'truth', ['*line', 'point']),
    ('Two', 'truth', ['*entity']),
    ('Three', 'truth', ['*entity']),
    ('Five', 'truth', ['*entity']),
    ('Six', 'truth', ['*entity']),
    ('BisectsAngle', 'truth', ['line', 'angle']),
    ('WhichOf', 'root', ['*root']),
    ('Following', '*root', []),
    ('What', 'number', []),
    ('AverageOf', 'number', ['*number']),
    ('SumOf', 'number', ['*number']),
    ('Twice', 'number', ['number']),
    ('RatioOf', 'number', ['number', 'number']),
    ('Integral', 'truth', ['number']),
    ('SquareOf', 'number', ['number']),
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

signatures = get_function_signatures()
signatures['What'] = VariableSignature('What', 'number')
signatures['Following'] = VariableSignature('Following', 'entity')