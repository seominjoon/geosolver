from geosolver.grounding.states import MatchParse
from geosolver.text2.ontology import FormulaNode, issubtype, VariableSignature, signatures

__author__ = 'minjoon'


def parse_match_atoms(match_parse):
    assert isinstance(match_parse, MatchParse)
    match_atoms = []
    for label, terms in match_parse.match_dict.iteritems():
        for term in terms:
            assert isinstance(term, FormulaNode)
            if issubtype(term.return_type, 'entity'):
                continue

            # FIXME : to be obtained by tag model
            try:
                left_term = float(label)
            except:
                vs = VariableSignature(label, 'number')
                left_term = FormulaNode(vs, [])

            atom = FormulaNode(signatures['Equals'], [left_term, term])
            match_atoms.append(atom)

    return match_atoms
