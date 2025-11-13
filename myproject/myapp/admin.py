from django.contrib import admin
from .models import Profile, Employee, Salary

# Register your models here.
admin.site.register(Profile)
admin.site.register(Employee)
admin.site.register(Salary)
