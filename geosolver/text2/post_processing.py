import re
import networkx as nx
from geosolver.text2.ontology import FormulaNode, VariableSignature, SetNode

__author__ = 'minjoon'


def filter_dummies(formula_nodes):
    """
    Remove (filter) formula nodes that were used to determine variable types
    e.g. IsLine, IsCircle, IsQuad, IsTriangle, etc.
    :param formula_nodes:
    :return:
    """
    dummies = ['IsLine', 'IsCircle', 'IsTriangle', 'IsQuad', 'IsAngle']
    new_nodes = []
    for formula_node in formula_nodes:
        if not formula_node.signature.id in dummies:
            new_nodes.append(formula_node)
    return new_nodes


def apply_trans(match_parse, formula_nodes):
    """
    Given a list of formulas, resolve transitivity by Is relation

    :param formula_nodes:
    :return:
    """
    graph = nx.Graph()
    explicit_sigs = set()
    for formula_node in formula_nodes:
        assert isinstance(formula_node, FormulaNode)
        if formula_node.signature.id != "Is":
            continue
        a_node, b_node = formula_node.children
        a_sig, b_sig = a_node.signature, b_node.signature
        if not isinstance(a_sig, VariableSignature):
            continue
        if not isinstance(b_sig, VariableSignature):
            continue
        graph.add_edge(a_sig, b_sig)
        p = re.compile("^([A-Z]+|[a-z])$")
        if p.match(a_sig.name):
            explicit_sigs.add(a_sig)
        if p.match(b_sig.name):
            explicit_sigs.add(b_sig)

    tester = lambda sig: sig in graph and any(nx.has_path(graph, sig, explicit_sig) for explicit_sig in explicit_sigs)
    getter = lambda sig: [explicit_sig for explicit_sig in explicit_sigs if nx.has_path(graph, sig, explicit_sig)][0]
    new_formula_nodes = [formula_node.replace_signature(tester, getter) for formula_node in formula_nodes
                         if formula_node.signature.id != 'Is']
    return new_formula_nodes

def apply_cc(formula_nodes):
    clusters = {}
    for formula_node in formula_nodes:
        if formula_node.signature.id != 'CC':
            continue
        a_node, b_node = formula_node.children
        a_sig, b_sig = a_node.signature, b_node.signature
        if a_sig not in clusters:
            clusters[a_sig] = []
        clusters[a_sig].append(b_sig)

    tester = lambda node: node.signature in clusters
    getter = lambda node: SetNode([node] + [FormulaNode(nbr, []) for nbr in clusters[node.signature]])
    new_formula_nodes = [formula_node.replace_node(tester, getter) for formula_node in formula_nodes
                         if formula_node.signature.id != 'CC']
    return new_formula_nodes

def apply_distribution(nodes):
    """
    If unary: just expand!
    If binary and same length: respectively
    if binary and one vs multi: expand for all
    use tester/getter to achieve this.

    :param formula_nodes:
    :return:
    """
    return [_apply_distribution(node) for node in nodes]

def _apply_distribution(node):
    if len(node.children) == 0:
        return node
    if isinstance(node, SetNode):
        return node
    node = FormulaNode(node.signature, [_apply_distribution(child) for child in node.children])

    if len(node.children) == 1:
        child_node = node.children[0]
        if isinstance(child_node, SetNode) and not node.signature.arg_types[0][0] != '*':
            children = [FormulaNode(node.signature, [child]) for child in child_node.children]
            return SetNode(children)
    elif len(node.children) == 2:
        a_node, b_node = node.children
        if isinstance(a_node, SetNode) and node.signature.arg_types[0][0] != '*' and isinstance(b_node, SetNode) and node.signature.arg_types[1][0] != '*':
            assert len(a_node.children) == len(b_node.children)
            children = [FormulaNode(node.signature, [a_node.children[index], b_node.children[index]]) for index in range(len(a_node.children))]
            return SetNode(children)
        elif isinstance(a_node, SetNode) and node.signature.arg_types[0][0] != '*' and isinstance(b_node, FormulaNode):
            children = [FormulaNode(node.signature, [child, b_node]) for child in a_node.children]
            return SetNode(children)
        elif isinstance(a_node, FormulaNode) and isinstance(b_node, SetNode) and node.signature.arg_types[1][0] != '*':
            children = [FormulaNode(node.signature, [a_node, child]) for child in b_node.children]
            return SetNode(children)

    return node



