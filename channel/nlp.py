import re

import networkx as nx

from channel.models import *

class AllTagGraph(object):
    def __init__(self):
        g = self.graph = nx.DiGraph()

    def _dependency(self):
        pass

    def _pagerank(self):
        pass

    def export(self):
        pass

class TagGraph(object):
    def __init__(self, text):
        self.text = text
        self.graph = self._generate_graph()

    def _generate_graph(self, text):
        tags = text_miner.get_match_tags(text)
        g = nx.DiGraph()
        for tag in tags:
            g.add_node()



    def add_tags(self, tags):
        pass

    def remove_tags(self, tags):
        pass

    def get_direct_tags(self):
        pass

    def get_related_tags(self):
        return self.graph

    def _pagerank(self):
        pass


class TextMiner(object):
    MIN_N = 2
    MAX_N = 7

    def __init__(self):
        terms = NounTag.objects.all()
        self.tags = frozenset(t.name for t in terms)

    def get_match_tags(self, text):
        "Return match tags in dict {'tag_name': occurrence}"
        matches = {}
        tokens = self._tokenize(text)
        for token in tokens:
            for t in self._ngram(token, self.MIN_N, self.MAX_N):
                if t in self.tags:
                    matches[t] = matches[t] + 1 if matches.has_key(t) else 1
        return matches

    def _tokenize(self, text):
        return re.split(r'\W+', text, flags=re.UNICODE)

    def _ngram(self, token, min_n, max_n):
        token_len = len(token)
        for i in xrange(token_len):
            for j in xrange(i+min_n, min(token_len, i+max_n)+1):
                yield token[i:j]

text_miner = TextMiner()