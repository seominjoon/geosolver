import geosolver.ontology.ontology_semantics as ontology_semantics
import numpy as np
from geosolver.text2.ontology import FunctionNode, VariableSignature, function_signatures

__author__ = 'minjoon'

class TempHandler(object):
    def __init__(self):
        self.variables = {}
        self.entities = []

    def number(self, name, init=None):
        assert name not in self.variables
        if init is None:
            init = np.random.rand()
        self.variables[name] = init
        vn = FunctionNode(VariableSignature(name, 'number'), [])
        return vn

    def point(self, name, init=None):
        x_name = name + "_x"
        y_name = name + "_y"
        assert x_name not in self.variables
        assert y_name not in self.variables
        if init is None:
            init = np.random.rand(2)
        x, y = self.number(x_name, init[0]), self.number(y_name, init[1])
        vn = self.apply('Point', x, y)
        self.entities.append(vn)
        return vn

    def line(self, p1, p2):
        return self.apply('Line', p1, p2)

    def circle(self, center, r=None, init=None):
        if init is None:
            init = np.random.rand()
        if r is None:
            r_name = "%s_r" % center.current
            r = self.number(r_name, init=init)
        return self.apply('Circle', center, r)

    def apply(self, name, *args):
        vn = FunctionNode(function_signatures[name], args)
        if name in ['Line', 'Circle']:
            self.entities.append(vn)
        return vn

    def vector_to_dict(self, vector):
        assert len(vector) == len(self.variables)
        return dict(zip(self.variables.keys(), vector))

    def dict_to_vector(self):
        return self.variables.values()

class VariableHandler(object):
    def __init__(self):
        self.variables = {}
        self.entities = []

    def number(self, name, init=None):
        assert name not in self.variables
        if init is None:
            init = np.random.rand()
        self.variables[name] = init
        vn = VariableNode(name, [])
        return vn

    def point(self, name, init=None):
        x_name = name + "_x"
        y_name = name + "_y"
        assert x_name not in self.variables
        assert y_name not in self.variables
        if init is None:
            init = np.random.rand(2)
        self.variables[x_name] = init[0]
        self.variables[y_name] = init[1]
        vn = VariableNode('Point', [VariableNode(x_name, []), VariableNode(y_name, [])])
        self.entities.append(vn)
        return vn

    def line(self, p1, p2):
        return self.apply('Line', p1, p2)

    def circle(self, center, r=None, init=None):
        if init is None:
            init = np.random.rand()
        if r is None:
            r_name = "%s_r" % center.current
            r = self.number(r_name, init=init)
        return self.apply('Circle', center, r)

    def apply(self, name, *args):
        vn = VariableNode(name, args)
        if name in ['Line', 'Circle']:
            self.entities.append(vn)
        return vn

    def vector_to_dict(self, vector):
        assert len(vector) == len(self.variables)
        return dict(zip(self.variables.keys(), vector))

    def dict_to_vector(self):
        return self.variables.values()


class VariableNode(object):
    # TODO : this can be replaced with the Ontology's FunctionNode
    def __init__(self, current, args):
        self.current = current
        self.args = args

    def is_leaf(self):
        return len(self.args) == 0

    def evaluate(self, assignment):
        if self.is_leaf():
            return assignment[self.current]
        else:
            evaluated_args = []
            for arg in self.args:
                if isinstance(arg, VariableNode):
                    evaluated_args.append(arg.evaluate(assignment))
                else:
                    evaluated_args.append(arg)
            return getattr(ontology_semantics, self.current)(*evaluated_args)

    def __add__(self, other):
        current = ontology_semantics.Add.__name__
        return VariableNode(current, [self, other])

    def __radd__(self, other):
        current = ontology_semantics.Add.__name__
        return VariableNode(current, [other, self])

    def __mul__(self, other):
        current = ontology_semantics.Mul.__name__
        return VariableNode(current, [self, other])

    def __rmul__(self, other):
        current = ontology_semantics.Mul.__name__
        return VariableNode(current, [other, self])

    def __sub__(self, other):
        current = ontology_semantics.Sub.__name__
        return VariableNode(current, [self, other])

    def __rsub__(self, other):
        current = ontology_semantics.Sub.__name__
        return VariableNode(current, [other, self])

    def __div__(self, other):
        current = ontology_semantics.Div.__name__
        return VariableNode(current, [self, other])

    def __rdiv__(self, other):
        current = ontology_semantics.Div.__name__
        return VariableNode(current, [other, self])

    def __pow__(self, power, modulo=None):
        current = ontology_semantics.Pow.__name__
        return VariableNode(current, [self, power])

    def __rpow__(self, power, modulo=None):
        current = ontology_semantics.Pow.__name__
        return VariableNode(current, [power, self])

    def __eq__(self, other):
        current = ontology_semantics.Equals.__name__
        return VariableNode(current, [self, other])

    def __ge__(self, other):
        current = ontology_semantics.Greater.__name__
        return VariableNode(current, [self, other])

    def __lt__(self, other):
        current = ontology_semantics.Less.__name__
        return VariableNode(current, [self, other])


