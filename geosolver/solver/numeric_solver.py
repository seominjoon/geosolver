from scipy.optimize import minimize
from geosolver.solver.variable_handler import VariableHandler, VariableNode
import numpy as np

__author__ = 'minjoon'


class NumericSolver(object):
    def __init__(self, variable_handler, prior_atoms, max_num_resets=10, tol=10**-3):
        self.variable_handler = variable_handler
        self.atoms = prior_atoms
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
        if not self.assigned:
            self.assignment = find_assignment(self.variable_handler, self.atoms, self.max_num_resets, self.tol)
            self.assigned = True
        if not self.assignment:
            return False
        return query_atom.evaluate(self.assignment).norm < self.tol

    def find_assignment(self, query_atom):
        return find_assignment(self.variable_handler, self.atoms + [query_atom], self.max_num_resets, self.tol)

    def evaluate(self, variable_node):
        if not self.assigned:
            self.assignment = find_assignment(self.variable_handler, self.atoms, self.max_num_resets, self.tol)
            self.assigned = True

        assert self.assignment is not None
        return variable_node.evaluate(self.assignment)


def query(variable_handler, prior_atoms, query_atom, max_num_resets=10, tol=10**-3, verbose=False):
    assert isinstance(variable_handler, VariableHandler)
    assert isinstance(query_atom, VariableNode)
    prior_assignment, prior_sat = find_assignment(variable_handler, prior_atoms, max_num_resets, tol, verbose)

    unique = prior_sat and query_atom.evaluate(prior_assignment).norm < tol
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
        return sum(atom.evaluate(variable_handler.vector_to_dict(vector)).norm for atom in atoms)

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


