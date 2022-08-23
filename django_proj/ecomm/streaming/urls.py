from unicodedata import name
from django.urls import path
from .views import *



urlpatterns=[
    path('',home,name="streaming-home"),
    path('category/<str:pk>',courseCat,name="streaming-categories"),
    path('course/<int:pk>',courseView,name="streaming-course"),
    path('enroll/',streamingEnroll,name="streaming-enroll"),
    path('completed',completedEnroll,name="streaming-enroll-complete"),
    path('enrolled-courses',enrolledCourses,name="streaming-enrolled"),
    path('lessons/<int:pk>',lessonsView,name="lessons-list")
]