from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from django.conf import settings
from django.db.models.fields import DecimalField
from django.db.models.fields.related import ManyToManyField

import uuid
import os

def deals_imagen_file_path(instance, filename):
    #genera pach para imagen 
    ext = filename.split('.')[-1]
    filename=f'{uuid.uuid4()}.{ext}'
    return os.path.join('uploads/deals/', filename)

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        #crea y guarda un nuevo usuario 
        if not email:
            raise ValueError('user no have email')

        user=self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
        
    def create_superuser(self, email, password):
        #crea super usuario 
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    #usuarios que soportan hacer login con email en ves de usuario 
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    object = UserManager()

    USERNAME_FIELD = 'email'
    
class Tag_Brand(models.Model):
    #modelo de tag para deals
    name = models.CharField(max_length=255)
    logo = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Deals(models.Model):
    #modelo de oferta 
    name=models.CharField(max_length=255)
    image = models.ImageField(null=True, upload_to=deals_imagen_file_path)
    price=DecimalField(max_digits=6, decimal_places=3)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

class store(models.Model):
    identifier = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    addres= models.CharField(max_length=255)
    Deals = ManyToManyField('Deals')
    Tag_Brand=ManyToManyField('Tag_brand')