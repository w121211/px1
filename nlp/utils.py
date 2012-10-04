import re

import networkx

from channel.models import *
from nlp.models import *

ALL_TAGS_GRAPH = networkx.read_edgelist('/Users/chi/git/textmining/export/wired_text_hubpagerank.edgelist',
                                        create_using=networkx.DiGraph())
def init_data():
    u, created = User.objects.get_or_create(username='autorobo', password='autorobo')
    for n in ALL_TAGS_GRAPH.nodes_iter():
        if ALL_TAGS_GRAPH.out_degree(n) == 0:
            NounTag.objects.get_or_create(name=n, sub_type='H', user=u)
        else:
            NounTag.objects.get_or_create(name=n, sub_type='T', user=u)

class BaseTagGraph(object):
    def __init__(self):
        self.graph = networkx.DiGraph()
#        self.graph = ALL_TAGS_GRAPH

    def _dependency(self):
        pass

    def _pagerank(self, loop=20):
        g = self.graph
        damping = 0.85
        num = g.number_of_nodes()

        # Assign initial pageranks
        pr = 1.0 / num
        for n in g.nodes_iter():
            g.node[n]['pr'] = pr

        # Compute pageranks
        while loop > 0:
            max_bias = None
            for n in g.nodes_iter():
                pr_sum = 0.0
                for u, v, d in g.in_edges_iter(n, data=True):
                    dep_sum = 0.0
                    for e in g.out_edges_iter(u, data=True):
                        dep_sum += e[2]['weight']
                    pr_sum += g.node[u]['pr'] * (d['weight'] / dep_sum)
                    # pr_sum += g.node[u]['pr'] / g.out_degree(u)
                pr = (1.0 - damping) / num + damping * pr_sum
                g.node[n]['pr'] = pr
            loop -= 1

    def export(self):
        networkx.write_graphml(self.graph, 'test.graphml')


class TagGraph(BaseTagGraph):
    def __init__(self, text=None):
        super(TagGraph, self).__init__()
        self.text = text
        self.direct_tags = set()
        self.related_tags = set()
        self.add_text(text) if text else None

        self.miner = TextMiner()

    def add_text(self, text):
        self.text = text
        tags = self.miner.get_match_tags(text)
        self.add_tags(tags.keys())

    def add_tags(self, tags):
        for tag in tags:
            if tag not in self.direct_tags:
                self.direct_tags.add(tag)
                edges = ALL_TAGS_GRAPH.edges(tag, data=True)
                self.graph.add_edges_from(edges)
        self._update_related_tags()

    def remove_tags(self, tags):
        for tag in tags:
            self.direct_tags.discard(tag)

    def _update_related_tags(self):
        self._pagerank()
        for n, d in self.graph.nodes_iter(data=True):
            if d['pr'] > 0.05:
                self.related_tags.add(n)


class TextMiner(object):
    MIN_N = 2
    MAX_N = 4

    def __init__(self):
        terms = NounTag.objects.all()
        self.tags = frozenset(t.name for t in terms)

    def get_match_tags(self, text):
        """
        Return match tags in dict: {'tag_name': occurrence}
        """
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