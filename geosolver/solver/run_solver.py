from geosolver.solver.numeric_solver import numeric_solver
from geosolver.solver.variable_handler import VariableHandler
import numpy as np

__author__ = 'minjoon'

def example_0():
    """
    AB = 8, BC = 3, CA = 4. Is this possible?
    :return:
    """
    vh = VariableHandler()
    A = vh.point('A')
    B = vh.point('B')
    C = vh.point('C')
    AB = vh.line(A, B)
    BC = vh.line(B, C)
    CA = vh.line(C, A)
    c = vh.apply('LengthOf', AB)
    a = vh.apply('LengthOf', BC)
    b = vh.apply('LengthOf', CA)
    p1 = vh.apply('Equals', a, 3)
    p2 = vh.apply('Equals', b, 4)
    p3 = vh.apply('Equals', c, 8)
    success, assignment = numeric_solver(vh, [p1, p2, p3], verbose=True)
    print success


def example_1():
    """
    AB is tangent to circle O, AO = BO = 1 and AB = sqrt(2). What is the radius of circle O?
    :return:
    """
    vh = VariableHandler()
    O = vh.point('O')
    A = vh.point('A')
    B = vh.point('B')
    AO = vh.line(A, O)
    BO = vh.line(B, O)
    AB = vh.line(A, B)
    cO = vh.circle(O)
    a = vh.apply('LengthOf', AO)
    b = vh.apply('LengthOf', BO)
    o = vh.apply('LengthOf', AB)
    p1 = vh.apply('Equals', a, 1)
    p2 = vh.apply('Equals', b, 1)
    p3 = vh.apply('Equals', o, np.sqrt(2))
    p4 = vh.apply('Tangent', AB, cO)
    success, assignment = numeric_solver(vh, [p1, p2, p3, p4], verbose=False)
    ans = vh.apply('RadiusOf', cO)
    print ans.evaluate(assignment), 1/np.sqrt(2)  # the latter is the true answer


def example_2():
    """
    Question ID: 1
    In the diagram at the right, circle O has a radius of 5, and CE = 2.
    Diameter AC is perpendicular to chord BD at E.
    What is the length of BD?
    :return:
    """
    vh = VariableHandler()
    A = vh.point('A')
    B = vh.point('B')
    C = vh.point('C')
    D = vh.point('D')
    E = vh.point('E')
    O = vh.point('O')
    CE = vh.line(C, E)
    AC = vh.line(A, C)
    BD = vh.line(B, D)
    cO = vh.circle(O)
    p1 = vh.apply('Equals', vh.apply('RadiusOf', cO), 5)  # Equals(RadiusOf(cO), 5))
    p2 = vh.apply('Equals', vh.apply('LengthOf', CE), 2)  # Equals(LengthOf(CE), 2)
    p3 = vh.apply('IsDiameter', AC, cO)
    p4 = vh.apply('IsChord', BD, cO)
    p5 = vh.apply('Perpendicular', AC, BD)
    p6 = vh.apply('PointLiesOnLine', E, AC)
    p7 = vh.apply('PointLiesOnLine', E, BD)
    ps = [p1, p2, p3, p4, p5, p6, p7]
    success, assignment = numeric_solver(vh, ps, verbose=False)
    ans = vh.apply('LengthOf', BD)
    print ans.evaluate(assignment), 8  # the latter is the true answer

if __name__ == "__main__":
    example_1()
