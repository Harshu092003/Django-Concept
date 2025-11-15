from django.contrib import admin

from .models import Employee, Profile, Salary

# Register your models here.
admin.site.register(Profile)
admin.site.register(Employee)
admin.site.register(Salary)
