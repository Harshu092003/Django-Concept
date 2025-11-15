from django.db import models
from django.utils import timezone


# Create your models here.
class Profile(models.Model):
    name = models.CharField(max_length=50)
    phone_no = models.IntegerField()

    def __str__(self):
        return self.name


class Employee(models.Model):
    emp_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=50)
    designation = models.CharField(max_length=50)
    age = models.IntegerField()
    join_date = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.designation})"


class Salary(models.Model):
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="salaries"
    )
    basic = models.DecimalField(max_digits=10, decimal_places=2)
    hra = models.DecimalField(max_digits=10, decimal_places=2)
    da = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.CharField(max_length=20)
    created_at = models.DateTimeField(default=timezone.now)

    def total_salary(self):
        return self.basic + self.hra + self.da - self.tax

    def __str__(self):
        return f"{self.employee.name} - {self.month}"
