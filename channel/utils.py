from channel.models import *
from django.db import IntegrityError
from django.db.models import Q

AUTO_USER_NAME = 'autorobo'
AUTO_USER_PWD = 'autorobo'
LIKE_TAG_NAME = 'like'

class BaseTagger(object):
    def _tag(self, object, tag, user):
        live_tag = LiveTag.objects.create(content_object=object, tag=tag, user=user)
        return live_tag

    def get_tag(self, name):
        return Tag.objects.get(name=name)


class FunctionTagger(BaseTagger):
    def __init__(self, tag_name):
        self.auto_user, created = User.objects.get_or_create(username=AUTO_USER_NAME, password=AUTO_USER_PWD)
        self.tag_obj, created = FunctionTag.objects.get_or_create(user=self.auto_user, name=tag_name)

    def tag(self, object):
        return self._tag(object, self.tag_obj, self.auto_user)


class LikeTagger(FunctionTagger):
    def search(self, queryset, user):
        "Get all objects which the user vote 'like'"
        qs = queryset.filter(tags__tag=self.tag_obj, tags__voters=user)
        return qs


class PinTagger(FunctionTagger):
    pass


class TrendTagger(FunctionTagger):
    pass


class TermTagger(BaseTagger):
    def search(self, queryset, tag_names):
        pass


class NounTagger(TermTagger):
    def bulk_tag(self, object, tag_names, user):
        pass

    def tag(self, object, tag_name, user):
        try:
            t = Tag.objects.get(name=tag_name)
        except Tag.DoesNotExist:
            t = NounTag.objects.create(name=tag_name, user=user)
        live_tag = self._tag(object, t, user)
        live_tag.voters.add(user)
        return live_tag

    def search(self, queryset, tag_names):
        "Compute an && query, get all objects tagged with given tags."
        for n in tag_names:
            queryset = queryset.filter(tags__tag__name=n)
        return queryset


class GeneralTagger(object):
    def __init__(self):
        self.like = LikeTagger(LIKE_TAG_NAME)
        self.noun = NounTagger()

    def search(self, queryset, tag_names, user=None):
        tag_names = set(tag_names)
        fun_names = [LIKE_TAG_NAME]
        fun_names = set(fun_names)
        if LIKE_TAG_NAME in tag_names and user:
            tag_names.remove(self.like.tag_obj.name)
            qs = self.like.search(queryset, user)
            if tag_names:
                # quere for 'like' & ('tt1' & 'tt2' & ...)
                qs = self.noun.search(qs, tag_names)
        else:
            tag_names -= fun_names
            qs = self.noun.search(queryset, tag_names)
        return qs

    def vote(self, live_tag_id, user):
        live_tag = LiveTag.objects.select_related().get(id=live_tag_id)
        live_tag.vote(user=user)
        return live_tag