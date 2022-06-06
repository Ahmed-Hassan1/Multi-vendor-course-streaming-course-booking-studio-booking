from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.mail import send_mail
# Create your models here.


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username=None
    email=models.EmailField(unique=True,null=True,default=None,max_length=50)
    phone_number=models.CharField(unique=True,null=True,blank=True,max_length=20)

    is_customer=models.BooleanField(default=False)
    is_vendor=models.BooleanField(default=False)
    
    USERNAME_FIELD= 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


#dublicate phone number and email here ? for convience
class Customer(models.Model):
    customuser=models.OneToOneField(CustomUser,on_delete=models.CASCADE,primary_key=True)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)

    def __str__(self):
        return self.customuser.email


class Vendor(models.Model):
    customuser=models.OneToOneField(CustomUser,on_delete=models.CASCADE,primary_key=True)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    company_name = models.CharField(max_length=100)

    is_activated = models.BooleanField(default=False)


    def __str__(self):
        return self.company_name

class VendorPayments(models.Model):
    vendor = models.ForeignKey(Vendor,on_delete=models.SET_NULL,null=True)
    payments = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if not self.vendor:
            return 'Deleted' 
        return self.vendor.company_name