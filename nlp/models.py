from django.db import models

class AllTagGraph(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    graph = models.TextField()

class GraphManager(models.Manager):
    def create_graph(self, file):
        g = None
        self.create(graph=g)

    def read_graph(self, file):
        pass