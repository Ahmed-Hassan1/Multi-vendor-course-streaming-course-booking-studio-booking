from django.db import models
from smart_selects.db_fields import ChainedForeignKey
from django.utils.text import slugify
from django.db.models.signals import pre_save
from accounts.models import Vendor, Customer

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200)
    homePageImage = models.ImageField(null=True,blank=True)
    BannerImage = models.ImageField(null=True,blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.homePageImage.url
        except:
            url = ''
        return url

    @property
    def imageURL_banner(self):
        try:
            url = self.BannerImage.url
        except:
            url = ''
        return url

class SubCategory(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    BannerImage = models.ImageField(null=True,blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL_banner(self):
        try:
            url = self.BannerImage.url
        except:
            url = ''
        return url

class Product(models.Model):
    #add date timestamp
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    subCategory = ChainedForeignKey(SubCategory,'category','category',False,True)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,null=True,blank=True,allow_unicode=True)
    price = models.FloatField()
    image = models.ImageField(null=True,blank=True)
    image2 = models.ImageField(null=True,blank=True)
    image3 = models.ImageField(null=True,blank=True)
    image4 = models.ImageField(null=True,blank=True)
    image5 = models.ImageField(null=True,blank=True)
    vendor = models.ForeignKey(Vendor,null=True,on_delete=models.CASCADE)
    activate = models.BooleanField(default=True,null=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    @property
    def image2URL(self):
        try:
            url = self.image2.url
        except:
            url = ''
        return url
    @property
    def image3URL(self):
        try:
            url = self.image3.url
        except:
            url = ''
        return url
    @property
    def image4URL(self):
        try:
            url = self.image4.url
        except:
            url = ''
        return url
    @property
    def image5URL(self):
        try:
            url = self.image5.url
        except:
            url = ''
        return url
    

import string
import random
def random_string_generator(size = 10, chars = string.ascii_lowercase + string.digits):
    print("RANDOM_STRING: ",''.join(random.choice(chars) for _ in range(size))) 
    return ''.join(random.choice(chars) for _ in range(size))

def unique_slug(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        print("INSTANCE_NAME: ",instance.name)
        slug = slugify(instance.name,allow_unicode=True)#allow unicode in slugify function
    print("UNIQUE_SLUG: ",slug)
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
    customer = models.ForeignKey(Customer,blank=True,null=True, on_delete=models.SET_NULL)
    date = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False,null=True)
    transaction_id = models.CharField(max_length=200,null=True)

    @property
    def get_total_price(self):
        orderitems = self.orderitem_set.all()
        total = sum([orderitem.price for orderitem in orderitems])
        return total
    
    @property
    def get_total_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([orderitem.quantity for orderitem in orderitems])
        return total

    def __str__(self):
        return str(self.id)+ " " + str(self.customer) 

class OrderItem(models.Model): # get total @property function
    choices=[
        ('Processing','Processing'),
        ('Shipping','Shipped'),
        ('Delivered','Delivered'),
    ]


    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    quantity = models.IntegerField(default=0)
    price = models.FloatField(default=0)
    
    status = models.CharField(max_length=15,choices=choices,default='Processing')
    
    @property
    def unit_price(self):
        return self.price/self.quantity

    def __str__(self):
        if not self.product:
            return str(self.id)+ " " "DELETED"
        return str(self.id)+ " " +self.product.name


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL,blank=True,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)


    telephone = models.CharField(max_length=50,null=False)
    name = models.CharField(max_length=200,null=False)
    address = models.CharField(max_length=250,null=False)
    city = models.CharField(max_length=50,null=False)
    state = models.CharField(max_length=50,null=False)

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