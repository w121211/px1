from django.db import models

class AllTagsGraph(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    graph = models.TextField()