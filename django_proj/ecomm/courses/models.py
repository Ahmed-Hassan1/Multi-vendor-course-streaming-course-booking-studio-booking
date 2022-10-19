from django.db import models
from smart_selects.db_fields import ChainedForeignKey
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
            url = self.BannerImage.url
        except:
            url = ''
        return url

class CourseSessions(models.Model):
    courseCategory=models.ForeignKey(CourseCategory,on_delete=models.CASCADE,blank=True,null=True)
    course=ChainedForeignKey(Course,'courseCategory','courseCategory',False,True)
    date = models.DateField()
    start_hour=models.CharField(max_length=20)
    end_hour=models.CharField(max_length=20)

    def __str__(self):
        return str(self.course) +" "+ str(self.courseCategory)


class CourseStudent(models.Model):
    student = models.ForeignKey(Customer,on_delete=models.CASCADE,blank=True,null=True)
    course = models.ForeignKey(Course,blank=True,null=True,on_delete=models.CASCADE)
    session = models.ForeignKey(CourseSessions,on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return self.student.first_name+" "+self.student.last_name + " enrolled In " + self.course.name