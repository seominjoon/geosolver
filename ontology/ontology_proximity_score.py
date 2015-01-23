from geosolver.ontology.get_ontology_graph_paths import get_ontology_graph_paths
from geosolver.ontology.states import Type, BasicOntology, Function

__author__ = 'minjoon'


def ontology_proximity_score(basic_ontology, from_type, to_obj):
    paths = get_ontology_graph_paths(basic_ontology, from_type, to_obj)
    if len(paths) == 0:
        return 0

    min_path = min(paths, key=lambda p: len(p))

    if isinstance(to_obj, Type):
        assert len(min_path) % 2 == 1
        return 2.0/(len(min_path)-1)
    elif isinstance(to_obj, Function):
        assert len(min_path) % 2 == 0
        return 2.0/len(min_path)
    else:
        raise Exception()


