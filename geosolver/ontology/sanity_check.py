"""
Sanity check for ontology definitions.

basic_definitions:
1. each type/symbol has only valid keys, and all mandatory keys, and no duplicate definitions of keys
2. no two type/symbol has same name
3. supertype of each type is predefined in types
4. arg_types and return_type of each symbol are defined in types
"""
import logging

__author__ = 'minjoon'


def visual_sanity_check():
    pass


def basic_sanity_check(types, symbols):
    if _basic_sanity_check(types, symbols):
        logging.info("Syntax verification of basic_ontology definitions completed with no error.")
    else:
        raise Exception("Ontology definitions are invalid; see logging.")


def _basic_sanity_check(types, symbols):

    type_mandatory_keys = {'name'}
    type_optional_keys = {'supertype', 'label'}
    type_keys = type_mandatory_keys.union(type_optional_keys)

    symbol_mandatory_keys = {'name', 'arg_types', 'return_type'}
    symbol_optional_keys = ['label']
    symbol_keys = symbol_mandatory_keys.union(symbol_optional_keys)

    type_names = set()
    for idx, type_ in enumerate(types):
        keys = set()
        for key in type_:
            if key not in type_keys:
                logging.error("Invalid key encountered: '%s' at type_defs:%d" % (key, idx))
                return False
            if key in keys:
                logging.error("Duplicate keys encountered: '%s' at type_defs:%d" % (key, idx))
                return False
            keys.add(key)
        if not type_mandatory_keys.issubset(keys):
            missing_keys = type_mandatory_keys.difference(keys)
            logging.error("Some mandatory keys are missing: %r at type_defs:%d" % (missing_keys, idx))
            return False
        if type_['name'] in type_names:
            logging.error("Non-unique name encountered: '%s' at type_defs:%d" % (type_['name'], idx))
            return False
        if 'supertype' in type_ and type_['supertype'] not in type_names:
            logging.error("Unknown 'supertype': '%s' at type %r" % (type_['supertype'], type_))
        type_names.add(type_['name'])

    symbol_names = set()
    for idx, symbol_ in enumerate(symbols):
        keys = set()
        for key in symbol_:
            if key not in symbol_keys:
                logging.error("Invalid key encountered: '%s' at function_defs:%d" % (key, idx))
                return False
            if key in keys:
                logging.error("Duplicate keys encountered: '%s' at function_defs:%d" % (key, idx))
                return False
            keys.add(key)
        if not symbol_mandatory_keys.issubset(keys):
            missing_keys = symbol_mandatory_keys.difference(keys)
            logging.error("Some mandatory keys are missing: %r at function %r" % (list(missing_keys), symbol_))
            return False
        if symbol_['name'] in symbol_names:
            logging.error("Non-unique name encountered: '%s' at function %r" % (symbol_['name'], symbol_))
            return False
        for arg_type in symbol_['arg_types']:
            if arg_type not in type_names:
                logging.error("Unknown arg type: '%s' at function %r" % (arg_type, symbol_))
                return False
        if symbol_['return_type'] not in type_names:
            logging.error("Unknown return type: '%s' at function %r" % (symbol_['return_type'], symbol_))
            return False

        symbol_names.add(symbol_['name'])

    # passed every test
    return True

