from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, first_name, email, phone_number, role, last_name=None, password= None):
        if not email:
            raise ValueError("User must have an email address")
        user= self.model(
            email= self.normalize_email(email),
            first_name= first_name,
            last_name= last_name,
            phone_number=phone_number,
            role=role,
        )
        user.set_password(password)
        user.save(using= self._db)
        return user
    
    def create_superuser(self, first_name, email, phone_number, last_name=None, password= None):
        user=self.create_user(
                email= self.normalize_email(email),
                first_name= first_name,
                last_name= last_name,
                phone_number= phone_number,
                role='Admin'
            )
        user.is_staff=True
        user.is_superuser=True
        user.save(using= self._db)
        return user