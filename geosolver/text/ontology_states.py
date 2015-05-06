__author__ = 'minjoon'

class FunctionSignature(object):
    def __init__(self, name, return_type, arg_types, is_symmetric=False):
        self.name = name
        self.return_type = return_type
        self.arg_types = arg_types
        self.is_symmetric = is_symmetric

    def is_leaf(self):
        return len(self.arg_types) == 0

    def is_unary(self):
        return len(self.arg_types) == 1

    def is_binary(self):
        return len(self.arg_types) == 2

    def __hash__(self):
        return hash((self.name, self.return_type, tuple(self.arg_types)))

    def __repr__(self):
        return "%s %s(%s)" % (self.return_type, self.name, ", ".join(self.arg_types))

    def __eq__(self, other):
        return repr(self) == repr(other)
