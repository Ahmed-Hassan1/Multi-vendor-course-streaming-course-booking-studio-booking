from django.shortcuts import render

# Create your views here.
def bookingHome(request):

    return render(request,'booking/bookinghome.html')