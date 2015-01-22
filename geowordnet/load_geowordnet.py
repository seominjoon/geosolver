from geosolver.geowordnet.states import Entry, GeoWordNet
__author__ = 'minjoon'


def load_geowordnet(basic_ontology, entry_defs):
    """
    Enumerate on entry with multiple lexemes

    :param geosolver.basic_ontology.states.BasicOntology basic_ontology:
    :param list entry_defs:
    :return GeoWordNet:
    """

    entries = []
    for entry_def in entry_defs:
        for lexeme in entry_def['lexemes']:
            entry = Entry(entry_def['lemma'], entry_def['pos'], basic_ontology.functions[lexeme])
            entries.append(entry)

    gwn = GeoWordNet(entries, basic_ontology)
    return gwn

