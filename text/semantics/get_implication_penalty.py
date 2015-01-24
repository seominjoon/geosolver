from geosolver.ontology.states import Type, OntologyPath
from geosolver.ontology.states import Function
from geosolver.ontology.states import BasicOntology

__author__ = 'minjoon'


def get_implication_penalty(basic_ontology, ontology_path):
    """
    In general, penalty = number of functions implied. (excluding start and end)
    However, penalty differs to prioritize some implications.

    Concretely,

    (number) -> [lengthOf ->] (line): -0.5
    (line) -> [line -> (reference) ->] AB: -0.5
    (point) -> [point -> (reference) ->] E: -0.5
    (number) -> [angleOf:arc ->] (arc): -0.5
    (number) -> [angleOf:angle ->] (angle): -0.5
    (truth) -> [exists ->] (entity): -1

    :param basic_ontology:
    :param ontology_path:
    :return:
    """
    assert isinstance(basic_ontology, BasicOntology)
    assert isinstance(ontology_path, OntologyPath)
    default_penalty = sum(1 for obj in ontology_path.nodes[1:-1] if isinstance(obj, Function))
    """
    Add different penalty here
    """
    for subpath in _get_subpaths(ontology_path.nodes, 3):
        if subpath[0] is basic_ontology.types['number']:
            if subpath[1] is basic_ontology.functions['lengthOf']:
                if subpath[2] is basic_ontology.types['line']:
                    default_penalty -= 0.5
            elif subpath[1] is basic_ontology.functions['angleOf:arc']:
                if subpath[2] is basic_ontology.types['arc']:
                    default_penalty -= 0.5
            elif subpath[1] is basic_ontology.functions['angleOf:angle']:
                if subpath[2] is basic_ontology.types['angle']:
                    default_penalty -= 0.5
        elif subpath[0] is basic_ontology.types['truth']:
            if subpath[1] is basic_ontology.functions['exists']:
                if basic_ontology.isinstance(subpath[2], basic_ontology.types['entity']):
                    default_penalty -= 1

    for subpath in _get_subpaths(ontology_path.nodes, 4):
        if subpath[0] is basic_ontology.types['line'] and \
                subpath[1] is basic_ontology.functions['line'] and \
                subpath[2] is basic_ontology.types['reference'] and \
                len(subpath[3].name) > 1:
            default_penalty -= 0.5
        if subpath[0] is basic_ontology.types['point'] and \
                subpath[1] is basic_ontology.functions['point'] and \
                subpath[2] is basic_ontology.types['reference'] and \
                len(subpath[3].name) == 1:
            default_penalty -= 0.5

    return default_penalty

def _get_subpaths(path, length):
    subpaths = []
    for start in range(0, len(path)-length+1):
        stop = start + length
        subpaths.append(path[start:stop])
    return subpaths


