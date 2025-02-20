import csv
from celery import shared_task
from movie.models import Movie, Genre, Actor
from django.db import transaction
from django.core.files import File
import os

@shared_task
def import_movies_from_csv(file_path):
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            title = row['title']
            description = row['description']
            release_date = row['release_date']
            rating = row.get('rating', None)
            duration = row['duration']
            poster_image_path = row.get('poster_image', None)
            genres = row['genres'].split(',')
            actors = row['actors'].split(',')

            with transaction.atomic():
                # Create or get the movie
                movie, created = Movie.objects.get_or_create(
                    title=title,
                    defaults={
                        'description': description,
                        'release_date': release_date if release_date else '2000-01-01',
                        'rating': rating,
                        'duration': duration
                    }
                )

                # Add poster image if provided
                if poster_image_path and os.path.exists(poster_image_path):
                    with open(poster_image_path, 'rb') as image_file:
                        movie.poster_image.save(os.path.basename(poster_image_path), File(image_file), save=True)

                # Add genres
                for genre_name in genres:
                    genre, _ = Genre.objects.get_or_create(name=genre_name.strip())
                    movie.genres.add(genre)

                # Add actors
                for actor_name in actors:
                    actor, _ = Actor.objects.get_or_create(name=actor_name.strip())
                    movie.actors.add(actor)

                movie.save()


