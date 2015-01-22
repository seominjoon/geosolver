"""
Sanity check for GeoWordNet definitions.

Ensures:
1. Only defined attributes are used, and all of them are used.
2. Only defined pos types are used.
3. Lexemes are defined in Ontology.
4. (warning) If all symbols are assigned lemmas.
"""
import logging

__author__ = 'minjoon'


def sanity_check(ontology, entries, attributes, pos_types):
    if _sanity_check(ontology, entries, attributes, pos_types):
        logging.info("Syntax verification of GeoWordNet definitions completed with no error.")
    else:
        raise Exception("GeoWordNet definitions are invalid; check logs.")


def _sanity_check(basic_ontology, entries, attributes, pos_types):
    """
    :param geosolver.basic_ontology.states.Ontology basic_ontology:
    :param list dictionary:
    :return bool:
    """

    symbol_name_set = frozenset(basic_ontology.symbols)
    attribute_set = frozenset(attributes)
    pos_type_set = frozenset(pos_types)

    lexemes = set()
    for entry in entries:
        assert isinstance(entry, dict)

        # 1
        curr_attribute_set = frozenset(entry.keys())
        if curr_attribute_set != attribute_set:
            logging.error("Missing attributes or unknown attributes: %r" % entry)
            return False

        # 2
        if entry['pos'] not in pos_type_set:
            logging.error("Unknown pos at %r" % entry)
            return False

        # 3
        for lexeme in entry['lexemes']:
            if lexeme not in symbol_name_set:
                logging.error("Unknown lexeme at %r" % entry)
                return False
            else:
                lexemes.add(lexeme)

    # 4
    lexeme_set = frozenset(lexemes)
    if lexeme_set != symbol_name_set:
        logging.warning("Some function_defs not referred by GeoWordNet: %r" % list(symbol_name_set.difference(lexeme_set)))

    return True
