from geosolver.ontology.ontology_definitions import SetNode

__author__ = 'minjoon'

CRITERIA = ['IsPoint', 'IsLine', 'IsCircle', 'IsPolygon', 'IsTriangle', 'IsQuad', 'IsHexagon', 'IntersectAt']

def flatten_formulas(formulas):
    out = []
    for formula in formulas:
        if isinstance(formula, SetNode):
            out.extend(formula.children)
        else:
            out.append(formula)
    return out

def filter_formulas(formulas, criteria=None):
    if criteria is None:
        criteria = CRITERIA
    out = []
    for formula in formulas:
        if not formula.signature.id in criteria:
            out.append(formula)
    return out
