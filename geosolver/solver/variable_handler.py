import numpy as np
from geosolver.text2.ontology import FunctionNode, VariableSignature, function_signatures

__author__ = 'minjoon'

class VariableHandler(object):
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
            r_name = "%s_r" % center.signature.id
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
