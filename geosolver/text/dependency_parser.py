"""
Interfaces for syntactic parsers.
That is, DO NOT implement the parser here.
Only provide interface here.
"""
from geosolver import settings
import requests
import networkx as nx
from geosolver.text.syntax.states import SyntaxTree
from geosolver.text.syntax.utils import match_trees

__author__ = 'minjoon'


class DependencyParser(object):

    def get_syntax_trees(self, words, k, unique=True):
        """
        Returns a list of (tree, score) pair in order of decreasing score
        """
        raise Exception("This function must be overriden!")

    def get_best_syntax_tree(self, words):
        return self.get_syntax_trees(words, 1)[0][0]


class StanfordParser(DependencyParser):
    """
    Connects to stanford parser sever via http.
    """
    def __init__(self, server_url):
        self.server_url = server_url

    def get_syntax_trees(self, words, k, unique=True):
        sentence = [words[index] for index in sorted(words.keys())]
        params = {'words': ' '.join(sentence), 'k': k, 'paragraph': ' '.join(sentence)}
        r = requests.get(self.server_url, params=params)
        data = r.json()

        tree_score_pairs = []

        for rank, tree_data in enumerate(data):
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
                    graph.node[from_]['label'] = "%s-%d" % (words[from_], from_)
                    graph.node[from_]['word'] = words[from_]

                if 'label' not in graph.node[to]:
                    graph.node[to]['label'] = "%s-%d" % (words[to], to)
                    graph.node[to]['word'] = words[to]

            if unique and not any(match_trees(syntax_tree.graph, graph) for syntax_tree in tree_score_pairs):
                tree_score_pairs.append((graph, score))

        return tree_score_pairs


stanford_parser = StanfordParser(settings.STANFORD_PARSER_SERVER_URL)