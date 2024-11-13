from django.urls import path
from .views import MovieList,MovieDetail,ReviewList,ReviewDetail,MovieRecommendation,MovieSearch


urlpatterns = [
    path('list/',MovieList.as_view(),name='movie-list' ),
    path('<int:pk>',MovieDetail.as_view(),name='movie-detail'),
    path('<int:pk>/reviews/',ReviewList.as_view(),name='review-list' ),
    path('reviews/<int:review_pk>',ReviewDetail.as_view(),name='review-list' ),
    path('recommended-movies/',MovieRecommendation.as_view(),name='recommended-movies' ),
    path('search/',MovieSearch.as_view(),name='search' ),
    
]