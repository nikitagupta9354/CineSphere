from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import MovieSerializer,ReviewSerializer
from .models import Movie
from .permissions import IsReviewOwnerOrReadOnly,IsAdminModeratorOrReadOnly
from .models import Movie, Review, Genre, Actor,Recommendation

from rest_framework.pagination import PageNumberPagination
from haystack.query import SearchQuerySet

# Create your views here.
class MovieList(APIView):
    permission_classes=[IsAdminModeratorOrReadOnly]
    def get(self,request):
        movies=Movie.objects.all()
        serializer=MovieSerializer(movies,many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer=MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class MovieDetail(APIView):
    permission_classes=[IsAdminModeratorOrReadOnly]
    def get(self,request,pk):
        movie=get_object_or_404(Movie,pk=pk)
        serializer=MovieSerializer(movie)
        return Response(serializer.data) 
    def put(self,request,pk):
        movie=get_object_or_404(Movie,pk=pk)
        serializer=MovieSerializer(movie,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk):
        movie=get_object_or_404(Movie,pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class ReviewList(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,pk):
       movie=get_object_or_404(Movie,pk=pk)
       reviews=Review.objects.filter(movie=movie).order_by('created_at')
       serializer=ReviewSerializer(reviews, many=True)
       return Response(serializer.data,status=status.HTTP_200_OK)
    def post(self,request,pk):
        movie=get_object_or_404(Movie,pk=pk)
        serializer=ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user,movie=movie)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class ReviewDetail(APIView):
    permission_classes=[IsReviewOwnerOrReadOnly]
    def get(self,request,review_pk):
        review=get_object_or_404(Review,pk=review_pk)
        self.check_object_permissions(request, review)
        serializer=ReviewSerializer(review)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def put(self,request,review_pk):
        review=get_object_or_404(Review,pk=review_pk)
        self.check_object_permissions(request, review)
        serializer=ReviewSerializer(review,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,review_pk):
        review=get_object_or_404(Review,pk=review_pk)
        self.check_object_permissions(request, review)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        

class MovieRecommendation(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        recommendation = get_object_or_404(Recommendation,user=request.user)
        recommended_movies=recommendation.recommended_movies.all()
        serializer=MovieSerializer(recommended_movies,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class MovieSearch(APIView):
    def get(self, request):
        search_query = request.query_params.get('search_query', None)
        genre = request.query_params.get('genre', None)
        sort_by = request.query_params.get('sort_by', None)
        
        sqs = SearchQuerySet().all()
        
        
        if search_query:
            sqs = sqs.filter(text=search_query)
            
            if not sqs:
                return Response({"message": "No movies found matching the search criteria."}, status=status.HTTP_404_NOT_FOUND)
            
            if genre:
                sqs = sqs.filter(genres=genre)
        
            if sort_by:
                sqs = sqs.order_by(-sort_by)
                
                

        paginator = PageNumberPagination()
        paginator.page_size = 10  
        result_page = paginator.paginate_queryset(sqs, request)

        movies = [hit.object for hit in result_page]
        serializer = MovieSerializer(movies, many=True)
        
        return paginator.get_paginated_response(serializer.data)





