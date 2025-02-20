from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from django.shortcuts import render
from django.http import JsonResponse
from .tasks import import_movies_from_csv
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt

class UploadMovieData(APIView):
    permission_classes=[IsAdminUser]
    @csrf_exempt
    def post(self, request):
        if request.FILES.get('file'):
            file = request.FILES['file']
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            file_path = fs.path(filename)
            import_movies_from_csv.delay(file_path)
            return JsonResponse({'message': 'Movie data is being imported asynchronously.'})

        return JsonResponse({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)
