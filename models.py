from django.contrib.auth.models import AbstractUser
from django.db import models

class AbstractUser(models.Model):
    first_name=models.CharField(max_length=20)
    last_name=models.CharField(max_length=20)
    email=models.CharField(max_length=20)
    username=models.CharField(max_length=20)
    password=models.CharField(max_length=20)
    



class User(AbstractUser):
    
    pass
