from random import randint
from django.http import JsonResponse
from django.shortcuts import render
from .models import *
from django.http import JsonResponse, HttpResponse
# Create your views here.
def Home(request):

    context={}

    return render(request,'booking/home.html',context)

def book(request):
    opendates = OpenDates.objects.all()
    temp_list=[]
    for x in opendates:
        temp_list.append(x.day)

    days = ['Saturday','Sunday','Monday','Tuesday','Wednsday','Thursday','Friday']

    ordered_days=[]
    for day in days:
        if day in temp_list:
            ordered_days.append(day)
    
    

    context={'opendates':opendates,'days':ordered_days}
    return render(request,'booking/book.html',context)


def getHours(request):
    day=request.GET['day']
    selected_date=request.GET['date']
    day_price = OpenDates.objects.get(day=day)
    if day == "default":
        return JsonResponse({"default":"default"})

    hours=OpenDates.objects.get(day=day)

    list_dates = Reservations.objects.all().filter(day=selected_date)
    HOUR_CHOICES=(
        ('0','12 am'),('1','1 am'),('2','2 am'),('3','3 am'),
        ('4','4 am'),('5','5 am'),('6','6 am'),('7','7 am'),
        ('8','8 am'),('9','9 am'),('10','10 am'),('11','11 am'),
        ('12','12 pm'),('13','1 pm'),('14','2 pm'),('15','3 pm'),
        ('16','4 pm'),('17','5 pm'),('18','6 pm'),('19','7 pm'),
        ('20','8 pm'),('21','9 pm'),('22','10 pm'),('23','11 pm'),
    )

    hours_to_remove=[]
    for res_date in list_dates:
        temp_list=[]
        for i in range(int(res_date.start_hour),int(res_date.end_hour)):
            temp_list.append(HOUR_CHOICES[i])
        hours_to_remove.append(temp_list)


    hours_list=[]
    for i in range(int(hours.start_hour),int(hours.end_hour)+1):
        hours_list.append(HOUR_CHOICES[i])
    for res_hour in hours_to_remove:
        for i in res_hour:
            if i in hours_list:
                hours_list.remove(i)
    return JsonResponse({"hours":hours_list,'day_price':day_price.price,'reserves':list(list_dates.values())})



def reserve(request):
    print(request.POST)
    reserve_number=reservation_unique_id()
    Reservations.objects.create(
        unique_id=reserve_number,
        name = request.POST['name'],
        phone = request.POST['phone'],
        day = request.POST['day'],
        start_hour = request.POST['start-hour'],
        end_hour = request.POST['end-hour'],
        price = request.POST['price'],
        status = 'Pending',
    )

    context={'reserve_number':reserve_number}
    return render(request,'booking/submit.html',context)

def reservation_unique_id():

    unique_ids=Reservations.objects.all()

    unique_flag=False
    while not unique_flag:
        unique=randint(1000000,9999999)
        unique_flag=True
        for unique_number in unique_ids:
            if unique == unique_number.unique_id:
                unique_flag=False
                break
        
        if unique_flag:
            return unique