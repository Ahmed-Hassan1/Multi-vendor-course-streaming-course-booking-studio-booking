import datetime
from dateutil.relativedelta import relativedelta
from django.db import models
from accounts.models import Customer
# Create your models here.

class CourseCategory(models.Model):
    name = models.CharField(max_length=200)


    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=200)
    courseCategory = models.ForeignKey(CourseCategory,on_delete=models.CASCADE,null=True)
    description = models.CharField(max_length=255,default="")
    image = models.ImageField(null=True,blank=True)
    price = models.FloatField()

    def __str__(self):
        return self.name

    @property
    def imageURL_banner(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class Lesson(models.Model):
    name = models.CharField(max_length=200)
    course = models.ForeignKey(Course,on_delete=models.CASCADE,blank=True,null=True)
    position = models.IntegerField()
    video = models.FileField()
    thumbnail = models.ImageField()

    def __str__(self):
        return self.name

class Enrollment(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE,blank=True,null=True)
    user = models.ForeignKey(Customer,on_delete=models.CASCADE,blank=True,null=True)

def expiration():
    return datetime.date.today()+relativedelta(months=1)

class Subscription(models.Model):
    STATUS=[
        ('complete','complete'),
        ('pending','pending'),
        ('cancelled','cancelled')
    ]

    enrollment= models.ForeignKey(Enrollment,on_delete=models.CASCADE,blank=True,null=True)
    payment_status = models.CharField(max_length=20,choices=STATUS)
    date = models.DateField(auto_now_add=True)
    expire= models.DateField(default=expiration)

