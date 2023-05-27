from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser
)

class MyUserManager(BaseUserManager):
   
   def create_user(self, email, first_name, surname, password=None,):
      if not email:
         raise ValueError('Users must have an email address')
      user = self.model(
      email=self.normalize_email(email),
      first_name = first_name,
      surname = surname
        )
      user.set_password(password)
      user.save(using=self._db)
      return user  
   
   def create_superuser(self, email, first_name, surname, password=None):
    """Creates and saves a superuser with the given email, password."""
    user = self.create_user(
       email,
       password=password,
       first_name = first_name,
       surname = surname
    )
    user.is_admin = True
    user.save(using=self._db)
    return user
        

class CustomUser(AbstractBaseUser):
    
    email = models.EmailField(
       verbose_name='email address',
       max_length=255,
       unique=True,
    )

    first_name = models.CharField(max_length=70, blank=False, null=False)
    surname = models.CharField(max_length=70, blank=False, null=False)
    other_name = models.CharField(max_length=70, blank=True)
    image = models.FileField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    
    objects = MyUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'surname']
    
    def __str__(self):
        return self.email



