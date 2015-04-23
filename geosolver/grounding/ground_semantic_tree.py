from collections import namedtuple
import itertools
import sympy
from geosolver.geowordnet.identify_constants import _get_number_score, _get_variable_score
from geosolver.grounding.states import MatchParse
from geosolver.ontology.states import Formula, Constant, Function
from geosolver.text.semantics.states import SemanticTree

__author__ = 'minjoon'

def ground_semantic_tree(match_parse, semantic_tree):
    """

    :param MatchParse match_parse:
    :param SemanticTree semantic_tree:
    :return tuple:
    """
    assert isinstance(semantic_tree, SemanticTree)
    assert isinstance(match_parse, MatchParse)
    text_formula = semantic_tree.formula
    basic_ontology = text_formula.basic_ontolgy
    grounded_semantic_trees = []


FormulaPack = namedtuple("FormulaPack", "formula variables cost")

def _ground_formula(match_parse, text_formula):
    """
    Helper function for ground_semantic_tree

    returns a tuple (grounded_formula, variables, cost)
    :param match_parse:
    :param formula:
    :return:
    """
    basic_ontology = text_formula.basic_ontolgy

    # Base cases: entity | number and constant | function | error
    current = text_formula.current  # current is either Constant or Function
    packs = []
    if isinstance(current, Constant) and basic_ontology.isinstance(current.type, basic_ontology.types['number']):
        # Either variable ('x', 'y', etc) or number ('1', '555', etc.)
        assert isinstance(current.content, str)
        number_cost = 1 - _get_number_score(current.content)
        variable_cost = 1 - _get_variable_score(current.content)
        if number_cost < 1:
            new_current = Constant(float(current.content), basic_ontology.types['number'])
            grounded_formula = Formula(basic_ontology, new_current, [])
            packs.append(FormulaPack(grounded_formula, {}, number_cost))

        if variable_cost < 1:
            variable = sympy.symbols(current.content)
            variables = {current.content: variable}
            new_current = Constant(variable, basic_ontology.types['number'])
            grounded_formula = Formula(basic_ontology, new_current, [])
            packs.append(FormulaPack(grounded_formula, variables, variable_cost))

    elif basic_ontology.isinstance(current.type, basic_ontology.types['entity']):
        # only single child
        packs.extend(_ground_entity(match_parse, text_formula))

    elif isinstance(current, Function):
        # Recursive case
        pack_list_of_list = [_ground_formula(match_parse, child) for child in text_formula.children]
        for pack_list in itertools.product(*pack_list_of_list):
            variables = {}
            cost = 0
            children = []
            for child, local_variables, local_cost in pack_list:
                children.append(child)
                cost += local_cost
                for key, value in local_variables.iteritems():
                    variables[key] = value
            grounded_formula = Formula(basic_ontology, current, children)
            packs.append(FormulaPack(grounded_formula, variables, cost))

    else:
        raise Exception("Something is wrong...")


def _ground_entity(match_parse, entity_formula):
    """

    :param match_parse:
    :param entity_formula:
    :return:
    """
    assert isinstance(entity_formula, Formula)
    current = entity_formula.current
    packs = []
    if isinstance(current, Constant):
        assert isinstance(current.content, tuple)
        packs.extend(_get_all(match_parse, current.type))
    elif isinstance(current, Function):
        assert len(entity_formula.children) == 1
        child = entity_formula.children[0]
        assert isinstance(child.current, Constant)
        if isinstance(child.current.content, tuple):
            packs.extend(_get_all(match_parse, child.current.type))
        elif isinstance(child.current.content, str):
            """
            Get specific entities
            """
            pass

    return packs

def _get_all(match_parse, type_):
    pass
