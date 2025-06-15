from django.contrib import admin
from .models import Course, Module

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at']
    search_fields = ['title']

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order']
    list_filter = ['course']

#@admin.register(Customuser)
#class CustomuserAdmin(admin.ModelAdmin):

