from collections import deque
from geosolver.text.ontology import function_signatures, issubtype
from geosolver.text.ontology_states import FunctionSignature

__author__ = 'minjoon'


class Node(object):
    def __init__(self, index, function_signature, children):
        assert isinstance(function_signature, FunctionSignature)
        for child in children:
            assert isinstance(child, Node)

        self.function_signature = function_signature
        self.children = children
        self.index = index

        # Ontology enforcement
        if self.function_signature.is_leaf():
            assert len(self.children) == 0
        else:
            for idx, child in enumerate(self.children):
                assert issubtype(child.function_signature.return_type, self.function_signature.arg_types[idx])

    def get_index(self, lift_index=False):
        if self.index is not None:
            return self.index
        if lift_index:
            if self.function_signature.is_leaf():
                return self.index
            elif self.function_signature.is_unary():
                return self.children[0].get_index(True)
            elif self.function_signature.is_binary():
                return self.index

    def iterate(self):
        """
        Iterate through all nodes, including self,
        and output (index, content), i.e. tag pair

        :return:
        """
        start = self
        queue = deque()
        queue.appendleft(start)
        while len(queue) > 0:
            out = queue.pop()
            assert isinstance(out, Node)
            yield out.index, out.function_signature
            for child in out.children:
                queue.appendleft(child)



    def __hash__(self):
        return hash(repr(self))
        """
        if self.function_signature.is_symmetric:
            return hash((self.index, self.function_signature, frozenset(self.children)))
        return hash((self.index, self.function_signature, tuple(self.children)))
        """

    def __eq__(self, other):
        """
        if self.function_signature.is_symmetric:
            return self.index == other.index and self.function_signature == other.function_signature and \
                   frozenset(self.children) == frozenset(other.children)
        """
        return repr(self) == repr(other)

    def __repr__(self):
        if self.index is None:
            index = 'i'
        else:
            index = str(self.index)
        if len(self.children) == 0:
            if self.function_signature.return_type == 'modifier':
                if self.function_signature.name in function_signatures:
                    return "%s@%s" % (self.function_signature.name, index)
                else:
                    return "'%s'@%s" % (self.function_signature.name, index)
            elif self.function_signature.return_type == 'number':
                return "[%s]@%s" % (self.function_signature.name, index)
            elif self.function_signature.return_type == 'variable':
                return "<%s>@%s" % (self.function_signature.name, index)
            else:
                return "%s@%s" % (self.function_signature.name, index)

        if self.function_signature.is_symmetric:
            args_string = ", ".join(string for string in sorted(repr(child) for child in self.children))
        else:
            args_string = ", ".join(repr(child) for child in self.children)
        return "%s@%s(%s)" % (self.function_signature.name, index, args_string)