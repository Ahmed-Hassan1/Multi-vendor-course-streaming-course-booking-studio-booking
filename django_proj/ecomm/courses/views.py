from django.shortcuts import render
from .models import *
# Create your views here.

def home(request):
    course_cats=CourseCategory.objects.all()
    courses = Course.objects.all()

    context={'course_cats':course_cats,'courses':courses}
    return render(request,'courses/home.html',context)

def courseCat(request,pk):
    cat = CourseCategory.objects.get(name=pk)
    courses=Course.objects.all().filter(courseCategory__name=cat)
    print(pk)
    context={'courseCat':cat,'courses':courses}
    return render(request,'courses/course_cat.html',context)

def courseView(request,pk):
    course = Course.objects.get(id=pk)
    courseCat= course.courseCategory
    context={'course':course,'courseCat':courseCat}
    return render(request,'courses/course.html',context)


def enrollConfirm(request):
    print(request.POST)
    courseCat_obj=CourseCategory.objects.get(name=request.POST['courseCat'])
    course_obj = Course.objects.get(name=request.POST['course'],courseCategory=courseCat_obj)
    CourseStudent.objects.create(
        student=request.user.customer,
        course=course_obj
    )
    return render(request,'courses/enroll.html')