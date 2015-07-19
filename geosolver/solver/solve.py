from geosolver.ontology.ontology_semantics import evaluate, Equals
from geosolver.solver.display_entities import display_entities
from geosolver.solver.numeric_solver import NumericSolver
from geosolver.ontology.ontology_definitions import FormulaNode

__author__ = 'minjoon'

def solve(given_formulas, choice_formulas=None, assignment=None):
    """

    :param list true_formulas:
    :param dict choice_formulas:
    :return:
    """
    #1. Find query formula in true formulas
    true_formulas = []
    query_formula = None
    for formula in given_formulas:
        assert isinstance(formula, FormulaNode)
        if formula.has_signature("What") or formula.has_signature("WhichOf") or formula.has_signature("Find"):
            if query_formula is not None:
                raise Exception("More than one query formula.")
            query_formula = formula
        else:
            true_formulas.append(formula)
    if query_formula is None:
        raise Exception("No query formula.")

    elif query_formula.has_signature("What"):
        ns = NumericSolver(true_formulas)
        ns.solve()
        out = {}
        if choice_formulas is None:
            # No choice given; need to find the answer!
            sf = query_formula.children[1]
            if sf.has_signature("What"):
                sf = query_formula.children[0]
            out = ns.evaluate(sf)
            return out
        for key, choice_formula in choice_formulas.iteritems():
            tester = lambda node: node.signature.id == "What"
            getter = lambda node: choice_formula
            replaced_formula = query_formula.replace_node(tester, getter)
            out[key] = ns.evaluate(replaced_formula)
        return out

    elif query_formula.has_signature("WhichOf"):
        tester = lambda node: isinstance(node, FormulaNode) and node.signature.id == "WhichOf"
        result = {}
        for choice, choice_formula in choice_formulas.iteritems():
            getter = lambda node: choice_formula
            replaced_formula = query_formula.replace_node(tester, getter)
            all_formulas = true_formulas + [replaced_formula]
            ns = NumericSolver(all_formulas)
            result[choice] = ns.evaluate(replaced_formula)
            print result[choice]
            if result[choice]:
                display_entities(ns)
        return result
