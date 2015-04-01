__author__ = 'minjoon'


def link_equations(equations, variable_links):
    """
    variable links contains information about which variable names should be considered equivalent (in sympy).
    For instance, we cab have line(AB) represented by  ((a, b), (c, d)), and point A reprsented by (e, f).
    Then there are two variable links: {'e': 'a', 'f': 'b'}
    Detailed implementation might change, but this is a rough intuition.

    Returns a list of equations, where equivalent variables should have same names.


    :param list equations:
    :param dict variable_links:
    :return list:
    """
