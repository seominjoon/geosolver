from _functools import partial
__author__ = 'minjoon'

from scipy.optimize import minimize
import sympy

def algebraic_solver(equation, initial_values):
    """
    Given a list of normalized sympy equations.
    Algebraically solve the system, i.e. returns a dictionary, e.g.
    {'a': 5, 'b': 10, 'c': 3}

    :param equations:
    :return dict:
    """
    indexToVariable = {i: var for (i,var) in enumerate(initial_values.keys())}
    evalExp = partial(evalFunctions, equation, indexToVariable)
    result = minimize(evalExp, initial_values.values(), method='SLSQP', options={'ftol': 10**-9, 'maxiter': 10000})
    
    return {indexToVariable[i]:val for (i,val) in enumerate(result.x)}
    
def evalFunctions(eq, indexToVariable, x):
    varToVal = {indexToVariable[i]: val for (i,val) in enumerate(x)}
    return eq(**varToVal) ** 2
# from geosolver.ontology.function_definitions_eval import *
# 
# def test(a,b,c,d,e,f,g,h):
#     ab = instantiators['point'](a,b)
#     cd = instantiators['point'](c,d)
#     ef = instantiators['point'](e,f)
#     gh = instantiators['point'](g,h)
#     return and_(isSquare(instantiators['quadrilateral'](ab,cd,ef,gh)), equal(lengthOf(instantiators['line'](ab,cd)), 3)).expression
#     
# print(algebraic_solver(test, {'a': 0, 'b': 0, 'c': 1, 'd': 0, 'e': 0, 'f': 1, 'g': 1, 'h': 1}))