from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .manager import UserManager
# Create your models here.

class User(AbstractBaseUser):
    ROLE_CHOICE= (
        ('Admin', 'Admin'),
        ('Moderator','Moderator'),
        ('User', 'User'),
    )
    first_name= models.CharField(max_length=50)
    last_name= models.CharField(max_length=50,blank=True,null=True)
    email= models.EmailField(max_length=100, unique=True)
    phone_number= models.CharField(max_length=12)
    role= models.CharField(max_length=10,choices= ROLE_CHOICE, default='User')
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    is_staff= models.BooleanField(default= False)
    is_superuser= models.BooleanField(default= False)
    is_active= models.BooleanField(default= True)
   

    USERNAME_FIELD= 'email'
    REQUIRED_FIELDS= ['first_name','phone_number']

    objects= UserManager()
    
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj= None):
        return self.is_staff
    
    def has_module_perms(self, app_label):
        return True
    
    
