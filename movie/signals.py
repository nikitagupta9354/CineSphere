from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Review, Movie, User,Recommendation
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

channel_layer = get_channel_layer()
#Sending movie notification 
@receiver(post_save, sender=Movie)
def send_movie_notification(sender, instance, created, **kwargs):
    if created:
        group_name = 'Movie_notifications'
        async_to_sync(channel_layer.group_send)(
        group_name, 
        {
            'type': 'send_movie_notification',
            'message':'Check out the new release!' ,
        }
    )
        

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
        recommendation, created = Recommendation.objects.get_or_create(user=instance.user)
        for genre in instance.movie.genres.all():
            movies=Movie.objects.filter(genres=genre).order_by('release_date')
            for movie in movies:
                if movie not in recommendation.recommended_movies.all():
                    recommendation.recommended_movies.add(movie)
        recommendation.save()
        
        #send recommendation notification
        group_name = f'user_{instance.user.id}_recommendation_notifications'
        async_to_sync(channel_layer.group_send)(
            group_name, 
            {
                'type': 'send_recommendation_notification',
                'message': 'New recommendations available!',
            }
        )

#Sending review notification       
@receiver(post_save, sender=Review)
def send_review_notification(sender, instance, created, **kwargs):
    if created:
        group_name = 'Review_notifications'
        async_to_sync(channel_layer.group_send)(
            group_name, 
            {
                'type': 'send_review_notification',
                'message': f'A new review has been posted for the movie {instance.movie.title}!',
            }
        )
                
        
        
        
