import collections

__author__ = 'minjoon'


def get_evalf_subs(variables, values):
    """
    variables is an arbitrary-depth dictionary of sympy variables.
    values has same dimension as variables, but contains values instead of variables.
    This returns 'subs' dictionary to be used when evaluating sympy expression written in variables.
    Ex. expr.evalf(subs=subs)
    :param dict variables:
    :param dict values:
    :return dict:
    """
    subs = {}
    for k, v in variables.items():
        if isinstance(v, collections.MutableMapping):
            subs = dict(subs.items() + get_evalf_subs(v, values[k]).items())
        else:
            subs[v] = values[k]
    return subs