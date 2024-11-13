from django.db import models
from user.models import User

class Genre(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Actor(models.Model):
    name = models.CharField(max_length=255)
    birth_date = models.DateField()
    biography = models.TextField()
    profile_image = models.ImageField(upload_to='actors/profile_images/', blank=True, null=True)
    
    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_date = models.DateField()
    rating = models.DecimalField(max_digits=3, decimal_places=1,blank=True, null=True)
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    poster_image = models.ImageField(upload_to='movies/posters/', blank=True, null=True)
    
    genres = models.ManyToManyField(Genre, blank=True)
    actors = models.ManyToManyField(Actor, blank=True)
    
    def __str__(self):
        return self.title


class Review(models.Model):
    user = models.ForeignKey(User,related_name='reviews', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie,related_name='reviews', on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(11)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Review for {self.movie.title} by {self.user.email}'
    
class Recommendation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    recommended_movies = models.ManyToManyField(Movie)
    def __str__(self):
        return f"Recommendations for {self.user.email}"