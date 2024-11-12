from django.forms import ValidationError
from rest_framework import serializers
from .models import User
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import password_validation
from .validators import StrongPasswordValidator


class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password=serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model= User
        fields=['email','first_name','last_name','phone_number','role','password','confirm_password']
        extra_kwargs = {
        'password':{'write_only':True}
        }
        
    def validate_password(self, value):
        try:
            password_validation.validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return password

        
    def validate(self, attrs):
        password=attrs.get('password')
        confirm_password=attrs.get('confirm_password')
        if password!=confirm_password:
            raise serializers.ValidationError("Passwords do not match")
        return attrs
    
    def create(self,validated_data):
        del validated_data['confirm_password']
        return User.objects.create_user(** validated_data)
    
class LoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=100)
    class Meta:
        model= User
        fields=['email','password']
        
class ResetPasswordEmailSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=100)
    class Meta:
        model= User
        fields=['email']
        
    def validate_email(self, value):
        user = User.objects.get(email=value)
        if not user:
            raise serializers.ValidationError({"You are not a registered user."})
        uid=urlsafe_base64_encode(force_bytes(user.id))
        token=PasswordResetTokenGenerator().make_token(user)
        request=self.context.get('request')
        relative_link = reverse('reset-password', kwargs={'uid': uid, 'token': token})
        absolute_url = request.build_absolute_uri(relative_link)
        print(settings.DEFAULT_FROM_EMAIL)
        send_mail('Password Reset', absolute_url, settings.DEFAULT_FROM_EMAIL, [user.email])
        return value
    
class ResetPasswordSerializer(serializers.ModelSerializer):
    new_password= serializers.CharField(style={'input_type':'password'}, write_only=True)
    confirm_new_password=serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model= User
        fields=['new_password','confirm_new_password']
        
    def validate_new_password(self, value):
        try:
            password_validation.validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return new_password
    
    def validate(self, attrs):
        new_password=attrs.get('new_password')
        confirm_new_password=attrs.get('confirm_new_password')
        if new_password!=confirm_new_password:
            raise serializers.ValidationError("Passwords do not match")
        try:
            id=smart_str(urlsafe_base64_decode(self.context.get('uid')))
            user=User.objects.get(id=id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError('Invalid UID')
        
        token=self.context.get('token')
        if not PasswordResetTokenGenerator().check_token(user,token):
            raise serializers.ValidationError('Token is invalid or expired')
        
        return attrs
    
    def save(self):
        id=smart_str(urlsafe_base64_decode(self.context.get('uid')))
        user=User.objects.get(id=id)
        password=self.validated_data['new_password']
        user.set_password(password)
        user.save()
    
    