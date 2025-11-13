from django.shortcuts import render
from django.http import JsonResponse , HttpResponse
from .models import Employee, Salary
from django.db.models import Sum,Q,F,Avg,Count,Max,Min

def show_employees(request):
    employee = Employee.objects.all()
    return JsonResponse(list(employee.values()), safe=False)

def filter_example(request):
    # Filter: IT department and age > 25
    it_employees = Employee.objects.filter(department="IT", age__gt=25) , # like similaraly can use lt , gte , lte , ne

    # Exclude inactive
    active_employees = Employee.objects.exclude(is_active=False)

    # icontains (case-insensitive match)
    name_match = Employee.objects.filter(name__icontains="ha")

    # startswith / endswith
    start = Employee.objects.filter(department__startswith="I")
    end = Employee.objects.filter(designation__endswith="er")

    data = {
        "it_employees": list(it_employees.values()),
        "active_employees": list(active_employees.values()),
        "name_match": list(name_match.values()),
        "startswith": list(start.values()),
        "endswith": list(end.values()),
    }
    return JsonResponse(data)


def aggregate_example(request):
    total_basic = Salary.objects.aggregate(Sum('basic'))
    avg_age = Employee.objects.aggregate(Avg('age'))
    dept_count = Employee.objects.values('department').annotate(total=Count('emp_id'))
    highest_da = Salary.objects.aggregate(Max('da'))

    data = {
        "total_basic": total_basic,
        "avg_age": avg_age,
        "department_counts": list(dept_count),
        "highest_da": highest_da,
    }
    return JsonResponse(data)

def update_example(request):
    # Update example
    Employee.objects.filter(name="Amit").update(department="QA")

    # F expression: increase basic by 10%
    Salary.objects.update(basic=F('basic') * 1.10)

    # Q object: active IT or HR employees
    q_result = Employee.objects.filter(Q(department="IT") | Q(department="HR"))  # Q object is used for complex queries using OR , AND , NOT operations

    # Delete example: remove inactive employees
    Employee.objects.filter(is_active=False).delete()

    data = {
        "updated_basic": list(Salary.objects.values('employee__name', 'basic')),
        "q_result": list(q_result.values('name', 'department')),
    }
    return JsonResponse(data)