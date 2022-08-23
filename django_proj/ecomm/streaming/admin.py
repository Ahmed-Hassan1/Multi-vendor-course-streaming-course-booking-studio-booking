from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(CourseCategory)
admin.site.register(Course)

admin.site.register(Enrollment)

class SubsctiptionAdmin(admin.ModelAdmin):
    readonly_fields=('date','expire')
admin.site.register(Subscription,SubsctiptionAdmin)


class lessonFilter(admin.ModelAdmin):
    list_filter=('course__name','course__courseCategory__name')

admin.site.register(Lesson,lessonFilter)