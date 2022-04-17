from django.db import models
from smart_selects.db_fields import ChainedForeignKey
from django.utils.text import slugify
from django.db.models.signals import pre_save
from accounts.models import Vendor, Customer

# Create your models here.

#Main Category Type of instrument
#Sub Category Instrument itself Oud,Guitar
#Product item itself

class Category(models.Model):
    name = models.CharField(max_length=200)
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

class SubCategory(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    #add date timestamp
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    subCategory = ChainedForeignKey(SubCategory,'category','category',False,True)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,null=True,blank=True)
    price = models.FloatField()
    image = models.ImageField(null=True,blank=True)
    vendor = models.ForeignKey(Vendor,null=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

import string
import random
def random_string_generator(size = 10, chars = string.ascii_lowercase + string.digits): 
    return ''.join(random.choice(chars) for _ in range(size))

def unique_slug(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.name)

    Klass = instance.__class__ 
    qs_exists = Klass.objects.filter(slug = slug).exists()
    if qs_exists:
        new_slug= "{slug}-{randString}".format(slug=slug,randString=random_string_generator())
        return unique_slug(instance,new_slug=new_slug)
    return slug

def pre_save_reciever(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug=unique_slug(instance)

pre_save.connect(pre_save_reciever,sender=Product)


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)#modify the delete to keep the records
    date = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False,null=True)

    @property
    def get_total_price(self):
        orderitems = self.orderitem_set.all()
        total = sum([orderitem.product.price for orderitem in orderitems])
        return total
    
    @property
    def get_total_items(self):
        orderitems = self.orderitem_set.all().count()
        return orderitems

class OrderItem(models.Model): # get total @property function
    choices=[
        ('Processing','Processing'),
        ('Shipped','Shipped'),
        ('Delivered','Delivered'),
    ]


    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    status = models.CharField(max_length=15,choices=choices,default='Processing')
    def __str__(self):
        return self.product.name


#Home page carousell and cards
class CarouselBanner(models.Model):
    name = models.CharField(max_length=200)
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