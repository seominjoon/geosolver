from scipy.optimize import minimize
import numpy as np

from geosolver.ontology.ontology_semantics import evaluate
from geosolver.solver.variable_handler import VariableHandler
from geosolver.text2.ontology import FunctionNode

__author__ = 'minjoon'


class NumericSolver(object):
    def __init__(self, prior_atoms, variable_handler=None, max_num_resets=10, tol=10**-3):
        if variable_handler is None:
            variable_handler = VariableHandler()
        self.variable_handler = variable_handler
        self.atoms = [variable_handler.add(prior_atom) for prior_atom in prior_atoms]
        self.max_num_resets = max_num_resets
        self.tol = tol
        self.assignment = None
        self.assigned = False

    def is_sat(self):
        if not self.assigned:
            self.assignment = find_assignment(self.variable_handler, self.atoms, self.max_num_resets, self.tol)
            self.assigned = True
        return self.assignment is not None

    def query_invar(self, query_atom):
        query_atom = self.variable_handler.add(query_atom)
        if not self.assigned:
            self.assignment = find_assignment(self.variable_handler, self.atoms, self.max_num_resets, self.tol)
            self.assigned = True
        if not self.assignment:
            return False
        return evaluate(query_atom, self.assignment).norm < self.tol

    def find_assignment(self, query_atom):
        query_atom = self.variable_handler.add(query_atom)
        return find_assignment(self.variable_handler, self.atoms + [query_atom], self.max_num_resets, self.tol)

    def evaluate(self, variable_node):
        variable_node = self.variable_handler.add(variable_node)
        if not self.assigned:
            self.assignment = find_assignment(self.variable_handler, self.atoms, self.max_num_resets, self.tol)
            self.assigned = True

        assert self.assignment is not None
        return evaluate(variable_node, self.assignment)


def query(variable_handler, prior_atoms, query_atom, max_num_resets=10, tol=10**-3, verbose=False):
    assert isinstance(variable_handler, VariableHandler)
    assert isinstance(query_atom, FunctionNode)
    prior_assignment, prior_sat = find_assignment(variable_handler, prior_atoms, max_num_resets, tol, verbose)

    unique = prior_sat and evaluate(query_atom, prior_assignment).norm < tol
    all_assignment, sat = find_assignment(variable_handler, prior_atoms + [query_atom], max_num_resets, tol, verbose)

    if unique:
        # If unique answer exists, then enforce satisfiability. Just in case of numerical errors.
        sat = True
        assignment = prior_assignment
    else:
        assignment = all_assignment

    return assignment, sat, unique


def find_assignment(variable_handler, atoms, max_num_resets, tol, verbose=False):
    init = variable_handler.dict_to_vector()

    def func(vector):
        return sum(evaluate(atom, variable_handler.vector_to_dict(vector)).norm for atom in atoms)

    for i in range(max_num_resets):
        result = minimize(func, init, method='SLSQP', options={'ftol': 10**-9, 'maxiter': 1000})
        if verbose:
            print("iteration %d:" % (i+1))
            print(result)
        fun = result.fun
        if fun < tol:
            break
        init = np.random.rand(len(init))

    if fun > tol:
        return None
    return variable_handler.vector_to_dict(result.x)
