from channel.models import *
from django.db.models import Q

class BaseTagger(object):
    def _tag(self, object, tag, user):
        l = LiveTag.objects.create(content_object=object, tag=tag, tagger=user)
        return l

    def get_tag(self, name):
        return Tag.objects.get(name=name)


class FunctionTagger(BaseTagger):
    tag_name = None
    tag_id = None
    auto_user = User.objects.get(username='auto')

    def __init__(self, tag_name):
        self.tag_name = tag_name
        self.tag_id = Tag.objects.get(name=tag_name).id

    def tag(self, object):
        LiveTag.objects.create(content_object=object, tag_id=self.tag_id, tagger=self.auto_user)


class LikeTagger(FunctionTagger):
    def search(self, queryset, user):
        '''
        Get all objects which the user vote 'like'
        '''
        qs = queryset.filter(tags__tag_id=self.tag_id, tags__voters=user)
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
#            t = self.get_tag(tag_name)
        except Tag.DoesNotExist:
            t = NounTag.objects.create(name=tag_name)
        l = self._tag(object, t, user)
        l.voters.add(user)

    def search(self, queryset, tag_names):
        '''
        Compute an && query, get all objects tagged with given tags.
        '''
        names = set(tag_names)
        qs = queryset.filter(tags__tag__type='NN')
        for n in names:
            qs = qs.filter(tags__tag__name=n)
        return qs


class GeneralTagger(object):
    like = LikeTagger('like')
    noun = NounTagger()

    def search(self, queryset, tag_names, user=None):
        names = set(tag_names)

        if self.like.name in names and user is not None:
            names.remove(self.like.name)
            qs = self.like.get_queryset(queryset, user)

            # quere for '#like' & ('#tt1' & '#tt2' & ...)
            if len(names) > 0:
                qs = self.term.get_queryset(qs, names)
        else:
            qs = self.term.get_queryset(queryset, names)
        return qs