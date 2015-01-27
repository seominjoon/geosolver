from geosolver.text.token_grounding.states import GroundedSyntaxPath, GroundedToken

__author__ = 'minjoon'

def get_grounded_syntax_path_cost(grounded_syntax_path):
    assert isinstance(grounded_syntax_path, GroundedSyntaxPath)
    cost = len(grounded_syntax_path)-1
    basic_ontology = grounded_syntax_path.basic_ontology
    entity = basic_ontology.types['entity']
    for idx, curr_token in enumerate(grounded_syntax_path.tokens[:-1]):
        next_token = grounded_syntax_path.tokens[idx+1]
        if isinstance(curr_token, GroundedToken) and isinstance(next_token, GroundedToken):
            curr_return_type = curr_token.function.return_type
            next_return_type = next_token.function.return_type
            if basic_ontology.isinstance(curr_return_type, entity) and next_return_type.name == 'reference':
                cost -= 1
            elif basic_ontology.isinstance(next_return_type, entity) and curr_return_type.name == 'reference':
                cost -= 1
    return cost
