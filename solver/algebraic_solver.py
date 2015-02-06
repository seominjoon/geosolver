from _functools import partial
__author__ = 'minjoon'

from scipy.optimize import minimize
import sympy

def algebraic_solver(equations, initial_values):
    """
    Given a list of normalized sympy equations.
    Algebraically solve the system, i.e. returns a dictionary, e.g.
    {'a': 5, 'b': 10, 'c': 3}

    :param equations:
    :return dict:
    """
    indexToVariable = {i: var for (i,var) in enumerate(initial_values.keys())}
    evalExp = partial(evalFunctions, equations, indexToVariable)
    result = minimize(evalExp, initial_values.values(), method='SLSQP', options={'ftol': 10**-9, 'maxiter': 10000})
    
    return {indexToVariable[i]:val for (i,val) in enumerate(result.x)}
    
def evalFunctions(equations, indexToVariable, x):
    varToVal = [(indexToVariable[i], val) for (i,val) in enumerate(x)]
    return sum(eq.subs(varToVal).evalf() ** 2 for eq in equations)

x = sympy.S(5)
y = sympy.S(1)/sympy.S(0)
print(max([x,y], key=lambda t:t.sort_key()))
print(algebraic_solver([sympy.S("x**2 - y**2"),sympy.S("x*y - x")], {sympy.S("x"):100, sympy.S("y"):5000}))