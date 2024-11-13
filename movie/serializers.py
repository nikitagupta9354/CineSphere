from rest_framework import serializers
from .models import Movie,Actor,Genre,Review


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['name', 'birth_date', 'biography', 'profile_image']
        
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name']

class MovieSerializer(serializers.ModelSerializer):
    actors = serializers.PrimaryKeyRelatedField(queryset=Actor.objects.all(), many=True)
    genres = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all(), many=True)
    class Meta:
        model = Movie
        fields = ['title', 'description', 'release_date', 'rating', 'duration', 'poster_image', 'genres', 'actors']
        
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['rating', 'comment']