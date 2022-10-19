from rest_framework import serializers
from store.models import Category, Product,SubCategory
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from accounts.models import CustomUser,Customer

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['id','name','imageURL']


class ProductSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=SubCategory
        fields=['id','name']

class ProductSerializer(serializers.ModelSerializer):
    category=serializers.StringRelatedField()
    subCategory=serializers.StringRelatedField()
    class Meta:
        model = Product
        fields=[
            'id','name','price','category','subCategory',
            'imageURL','image2URL','image3URL','image4URL','image5URL'
            ]


class CustomUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    first_name=serializers.CharField()
    last_name=serializers.CharField()
    phone_number=serializers.CharField()
    password=serializers.CharField(min_length=9,write_only=True)

    class Meta:
        model=CustomUser
        fields=('email','password','phone_number','first_name','last_name')
        extra_kwargs={'password':{'write_only':True}}

    def create(self, validated_data):
        password=validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        print("Instance1: ",instance.email)
        
        if password is not None:
            instance.set_password(password)
            instance.is_customer=True
            instance.phone_number=self.validated_data.get('phone_number')
        print("Instance2: ",instance)
        instance.save()
        customer=Customer.objects.create(customuser=instance)
        customer.first_name=self.validated_data.get('first_name')
        customer.last_name=self.validated_data.get('last_name')
        customer.save()

        return instance




#Token serializer
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls,user):
        token = super(MyTokenObtainPairSerializer,cls).get_token(user)

        token['first_name']=user.customer.first_name

        return token