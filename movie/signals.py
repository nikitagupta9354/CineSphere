from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Review, Movie, User,Recommendation

@receiver(post_save, sender=Review)
def update_movie_rating(sender, instance, created, **kwargs):
    movie = instance.movie
    all_reviews = movie.reviews.all()
    total_weighted_rating = 0
    total_weights = 0
    active_user_threshold = 5
    
    for review in all_reviews:
        user = review.user
        if user.reviews.count() > active_user_threshold:
           weight = 2
        else:
           weight = 1
        
       
        total_weighted_rating += review.rating * weight
        total_weights += weight
    
   
    weighted_average_rating = total_weighted_rating / total_weights
    
    
    movie.rating = weighted_average_rating
    movie.save()
    
@receiver(post_save, sender=Review)
def update_recommendations(sender, instance, created, **kwargs):
    
    if created:
        user = instance.user
        recommendation, created = Recommendation.objects.get_or_create(user=user)
        for genre in instance.movie.genres.all():
            movies=Movie.objects.filter(genres=genre).order_by('release_date')
            for movie in movies:
                if movie not in recommendation.recommended_movies.all():
                    recommendation.recommended_movies.add(movie)
        recommendation.save()
                
                
        
        
        
