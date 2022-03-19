from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()

    tag_choice = [('Oud','Oud'),('Guitar','Guitar'),('Tabla','Tabla')]
    tag = models.CharField(max_length=50,choices=tag_choice,null=True)

    image = models.ImageField(null=True,blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url