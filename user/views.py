import time
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .serializers import LoginSerializer, RegistrationSerializer
from .utils import get_tokens_for_user, send_sms
from .models import User
from .serializers import ResetPasswordEmailSerializer,ResetPasswordSerializer
# Create your views here.

class Registration(APIView):
    def post(self, request):
        serializer=RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response({'Registration Successful'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class Login(APIView):
    def post(self, request):
        serializer=LoginSerializer(data=request.data)
        if serializer.is_valid():
            email=serializer.data.get('email')
            password=serializer.data.get('password')
            user=authenticate(username=email,password=password)
            if user:
                otp = send_sms(user)
                request.session['otp'] = otp
                request.session['otp_expiration']=time.time()+300
                request.session['user_id'] = user.id
                return Response({'Message':'SMS sent for authentication','otp':otp},status=status.HTTP_200_OK)
            return Response({'Invalid credentials'},status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)
    
class VerifyOTP(APIView):
    def post(self, request):
        entered_otp = request.data.get('otp')
        stored_otp = request.session.get('otp')
        expiration_time = request.session.get('otp_expiration')
        user_id=request.session.get('user_id')
        user=User.objects.get(id=user_id)

        if not stored_otp or time.time() > expiration_time:
            return Response({"error": "OTP expired or invalid"}, status=400)

        
        if entered_otp == str(stored_otp):
            token=get_tokens_for_user(user)
            return Response({'token':token,'Message':'Login successful'})
        else:
            return Response({"error": "Invalid OTP"}, status=400)
        
class ResetPasswordEmail(APIView):
    def post(self, request):
        serializer=ResetPasswordEmailSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            return Response({'Message':'Password Reset Link Sent'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class ResetPassword(APIView):
    def post(self, request, uid, token):
        serializer=ResetPasswordSerializer(data=request.data,context={'uid':uid,'token':token})
        if serializer.is_valid():
            serializer.save()
            return Response({'Message':'Password Reset Successfully'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
