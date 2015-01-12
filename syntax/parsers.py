"""
Interfaces for syntactic parsers.
That is, DO NOT implement the parser here.
Only provide interface here.
"""
from geosolver import settings

__author__ = 'minjoon'


class DependencyParser(object):

    def parse_tree_score_pairs(self, tokens):
        pass


class StanfordParser(DependencyParser):
    """
    Connects to stanford parser sever via http.
    """
    def __init__(self, server_url):
        self.server_url = server_url

    def parse_tree_score_pairs(self, tokens):
        pass


stanford_parser = StanfordParser(settings.STANFORD_PARSER_SERVER_URL)