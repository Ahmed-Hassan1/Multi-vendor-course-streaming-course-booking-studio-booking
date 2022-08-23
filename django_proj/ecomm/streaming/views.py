from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.decorators import allowed_user
from .models import *
# Create your views here.

def home(request):
    course_cats=CourseCategory.objects.all()
    courses = Course.objects.all()

    context={'course_cats':course_cats,'courses':courses}
    return render(request,'streaming/home.html',context)

def courseCat(request,pk):
    cat = CourseCategory.objects.get(name=pk)
    courses=Course.objects.all().filter(courseCategory__name=cat)
    print(pk)
    context={'courseCat':cat,'courses':courses}
    return render(request,'streaming/course_cat.html',context)

def courseView(request,pk):
    course = Course.objects.get(id=pk)
    courseCat= course.courseCategory
    lessons = Lesson.objects.all().filter(course=course)
    enrolled=''
    if request.user.is_authenticated:
        
        if request.user.is_customer:
            try:
                enrolled  = Enrollment.objects.get(user=request.user.customer)
            except:
                enrolled=''
        else:
            enrolled=''

    context={'course':course,'courseCat':courseCat,'lessons':lessons,'enrolled':enrolled}
    return render(request,'streaming/course.html',context)


def streamingEnroll(request):
    print(request.POST)
    course = Course.objects.get(name=request.POST['course'])

    context={'course':course}
    return render(request,'streaming/streaming_enroll.html',context)

def completedEnroll(request):
    course = Course.objects.get(name=request.POST['course-name'])

    enrollment_obj=Enrollment.objects.create(
        course=course,
        user = request.user.customer
    )

    sub=Subscription.objects.create(
        enrollment=enrollment_obj,
        payment_status='complete'
    )
    return render(request,'streaming/complete_enroll.html')


@login_required(login_url='signin')
@allowed_user(roles=['Customer'])
def enrolledCourses(request):

    try:
        enrolled  = Enrollment.objects.all().filter(user=request.user.customer)
        subsrciption = Subscription.objects.all().filter(enrollment__user=request.user.customer)
    except Exception as e:
        print(e)
        enrolled=''
        subsrciption=''

    print(enrolled)
    print(subsrciption)
    context={'enrolled':enrolled,'subsrciption':subsrciption}
    return render(request,'streaming/enrolled_courses.html',context)

@login_required(login_url='signin')
@allowed_user(roles=['Customer'])
def lessonsView(request,pk):
    course = Course.objects.get(id=pk)
    lessons = Lesson.objects.all().filter(course=course).order_by("position")

    context={'course':course,'lessons':lessons}
    return render(request,'streaming/lessons_list.html',context)