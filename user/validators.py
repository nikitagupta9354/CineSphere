
from rest_framework import serializers


class StrongPasswordValidator:
    def validate(self,value,user=None):
            if len(value) < 8:
                raise serializers.ValidationError("Password should be at least 8 characters long")
            
            # Check for at least one digit
            if not any(char.isdigit() for char in value):
                raise serializers.ValidationError("Password should contain at least one digit")
            
            # Check for at least one letter
            if not any(char.isalpha() for char in value):
                raise serializers.ValidationError("Password should contain at least one letter")
            
            # Check for at least one uppercase letter
            if not any(char.isupper() for char in value):
                raise serializers.ValidationError("Password should contain at least one uppercase letter")
            
            # Check for at least one lowercase letter
            if not any(char.islower() for char in value):
                raise serializers.ValidationError("Password should contain at least one lowercase letter")
            
            # Check for at least one special character
            if not any(char in '@$!%*?&' for char in value):
                raise serializers.ValidationError("Password should contain at least one special character (@, $, !, %, *, ?, &)")
            
            return value