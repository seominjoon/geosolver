"""
Interfaces for syntactic parsers.
That is, DO NOT implement the parser here.
Only provide interface here.
"""
from geosolver import settings
import requests
import networkx as nx
from geosolver.text.syntax.states import TreeScorePair

__author__ = 'minjoon'


class DependencyParser(object):

    def parse_tree_score_pairs(self, tokens, k):
        """
        Parses top k trees given tokens
        """
        pass


class StanfordParser(DependencyParser):
    """
    Connects to stanford parser sever via http.
    """
    def __init__(self, server_url):
        self.server_url = server_url

    def parse_tree_score_pairs(self, tokens, k):
        sentence = tokens[0].sentence
        params = {'words': ' '.join(sentence), 'k': k, 'paragraph': ' '.join(sentence)}
        r = requests.get(self.server_url, params=params)
        data = r.json()

        tree_score_pairs = []

        for tree_data in data:
            score = tree_data['score']
            tuples = tree_data['tuples']
            graph = nx.DiGraph()
            for label, from_, to in tuples:
                from_ -= 1
                to -= 1
                if from_ < 0:
                    continue
                graph.add_edge(from_, to, label=label)
                if 'label' not in graph.node[from_]:
                    graph.node[from_]['label'] = "%s-%d" % (sentence[from_], from_)
                    graph.node[from_]['token'] = tokens[from_]
                if 'label' not in graph.node[to]:
                    graph.node[to]['label'] = "%s-%d" % (sentence[to], to)
                    graph.node[to]['token'] = tokens[to]

            tree_score_pairs.append(TreeScorePair(graph, score))

        return tuple(tree_score_pairs)


stanford_parser = StanfordParser(settings.STANFORD_PARSER_SERVER_URL)