from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self,first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError("User must have an email address")
        if not username:
            raise ValueError("User must have an username")

        user = self.model(
            email=self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )
        user.set_password(password)
        user.save(self._db)
        return user
    
    # def create_superuser(self,first_name,last_name,email,username,password):
    #     user = self.create_user(
    #         eamil = self.normalize_email(email),
    #         username = username,
    #         password=password, 
    #         first_name = first_name,
    #         last_name = last_name,
    #     )
    #     user.is_admin=True
    #     user.is_staff=True
    #     user.is_superuser=True
    #     user.is_active=True
    #     user.save(using=self._db)
    #     return user

    def create_superuser(self,first_name,last_name,email,username,password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff=True
        user.is_superuser = True
        user.save(using = self._db)
        return user
        




class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255,unique=True)
    email = models.EmailField(max_length=255,unique=True)
    phone = models.CharField(max_length=255)

    #required field
    joined_date = models.DateTimeField(auto_now_add=True)
    last_logging = models.DateTimeField(auto_now_add = True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    #replace username to email for logging
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username' ,'first_name','last_name']

    objects = MyAccountManager()

    def __str__(self):
        return self.first_name
    
    def has_perm(self,prem,obj=None):
        return self.is_admin
    
    def has_module_perms(self,add_label):
        return True

