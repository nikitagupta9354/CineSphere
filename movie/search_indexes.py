from haystack import indexes
from .models import Movie

class MovieIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    description = indexes.CharField(model_attr='description')
    release_date = indexes.DateField(model_attr='release_date')
    rating = indexes.DecimalField(model_attr='rating', null=True)
    duration = indexes.IntegerField(model_attr='duration', null=True)
    genres = indexes.MultiValueField()
    actors = indexes.MultiValueField()

    def get_model(self):
            return Movie

    def prepare_genres(self, obj):
        return [genre.name for genre in obj.genres.all()]

    def prepare_actors(self, obj):
        return [actor.name for actor in obj.actors.all()]

    def index_queryset(self, using=None):
        return self.get_model().objects.all()