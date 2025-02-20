from django.urls import path
from .views import UploadMovieData

urlpatterns = [
    path('upload/',UploadMovieData.as_view() , name='import-data'),
]