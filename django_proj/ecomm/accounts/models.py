from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    is_customer=models.BooleanField(default=False)
    is_vendor=models.BooleanField(default=False)
    


class Customer(models.Model):
    customuser=models.OneToOneField(CustomUser,on_delete=models.CASCADE,primary_key=True)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    phone_number=models.CharField(max_length=20)


class Vendor(models.Model):
    customuser=models.OneToOneField(CustomUser,on_delete=models.CASCADE,primary_key=True)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    company_name = models.CharField(max_length=100)
    phone_number=models.CharField(max_length=20)