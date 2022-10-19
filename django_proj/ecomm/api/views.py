from datetime import datetime
from django.http import JsonResponse
from .serializer import *
from store.models import *
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
# Create your views here.


def api_home(request):
    products = Product.objects.all()[:8]
    mainCats=Category.objects.all()
    product_serial=ProductSerializer(products,many=True)
    mainCats_serial=ProductCategorySerializer(mainCats,many=True)
    #print(JsonResponse([product_serial.data,mainCats_serial.data],safe=False))
    return JsonResponse([product_serial.data,mainCats_serial.data],safe=False)

def api_mainCat(request,pk):
    print(pk)

    subCats=SubCategory.objects.all().filter(category__id=pk)
    subCats_serial=ProductSubCategorySerializer(subCats,many=True)

    products= Product.objects.filter(category__id=pk)
    product_serial=ProductSerializer(products,many=True)

    return JsonResponse([product_serial.data,subCats_serial.data],safe=False)

def api_subCat(request,pk):
    products = Product.objects.filter(subCategory__id=pk)

    products_serial=ProductSerializer(products,many=True)

    return JsonResponse(products_serial.data,safe=False)

@api_view()
def api_protected_test(request):
    print(datetime.now())
    return JsonResponse({"Hello":"World"})

class hello(APIView):
    def get(self,request):
        return Response(data={"hello":"world"},status=status.HTTP_200_OK)



class ObtainTOkenPairWithFirstName(TokenObtainPairView):
    
    serializer_class = MyTokenObtainPairSerializer

class CustomerCreate(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self,request,format='json'):
        if Customer.objects.filter(customuser__email=str(request.data['email'])).exists():
            return Response({"error":"User already exists"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        serializer=CustomUserSerializer(data=request.data)
        print("Serial: ",serializer)
        if serializer.is_valid():
            user=serializer.save()
            if user:
                json=serializer.data
                print(json)
                return Response(json,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)