from scipy.optimize import minimize
from geosolver.solver.variable_handler import VariableHandler
import numpy as np

__author__ = 'minjoon'

def numeric_solver(variable_handler, atoms, max_num_resets=10, tol=10**-3, verbose=False):
    assert isinstance(variable_handler, VariableHandler)
    init = variable_handler.dict_to_vector()

    def func(vector):
        return sum(atom.evaluate(variable_handler.vector_to_dict(vector)).norm for atom in atoms)

    for i in range(max_num_resets):
        result = minimize(func, init, method='SLSQP', options={'ftol': 10**-9, 'maxiter': 1000})
        fun = result.fun
        if fun < tol:
            break
        init = np.random.rand(len(init))

    success = fun < tol
    assignment = variable_handler.vector_to_dict(result.x)
    if verbose:
        print "number of resets: %d" % i
        print result
    return success, assignment


