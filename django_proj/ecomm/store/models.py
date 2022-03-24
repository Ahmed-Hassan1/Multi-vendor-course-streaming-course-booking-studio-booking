from django.db import models
from smart_selects.db_fields import GroupedForeignKey,ChainedForeignKey

# Create your models here.

#Main Category Type of instrument
#Sub Category Instrument itself Oud,Guitar
#Product item itself

class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    subCategory = ChainedForeignKey(SubCategory,'category','category',False,True)
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