from django.db.models import Avg, Count, F, Max, Min, Q, Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from .models import Employee, Salary


def show_employees(request):
    employee = Employee.objects.all()
    return JsonResponse(list(employee.values()), safe=False)


def filter_example(request):
    # Filter: IT department and age > 25
    it_employees = (
        Employee.objects.filter(department="IT", age__gt=25),
    )  # like similaraly can use lt , gte , lte , ne

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
    total_basic = Salary.objects.aggregate(Sum("basic"))
    avg_age = Employee.objects.aggregate(Avg("age"))
    dept_count = Employee.objects.values("department").annotate(total=Count("emp_id"))
    highest_da = Salary.objects.aggregate(Max("da"))

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
    Salary.objects.update(basic=F("basic") * 1.10)

    # Q object: active IT or HR employees
    q_result = Employee.objects.filter(
        Q(department="IT") | Q(department="HR")
    )  # Q object is used for complex queries using OR , AND , NOT operations

    # Delete example: remove inactive employees
    Employee.objects.filter(is_active=False).delete()

    data = {
        "updated_basic": list(Salary.objects.values("employee__name", "basic")),
        "q_result": list(q_result.values("name", "department")),
    }
    return JsonResponse(data)


def chat(request):
    return render(request, "lobby.html")


from django.shortcuts import render


def sound(request):
    """
    Main view to render the sound transcript page with waveform,
    segments visualization, and spectrogram
    """
    # Sound file metadata
    soundfile = {
        "filename": "ps6_04_202.wav",
        "sample_rate": "48 KHz",
        "channels": "1 (mono)",
        "bit_depth": "32-bit",
        "duration": "05:22.340",
        "current_time": "00:00.000",  # Changed to start from beginning
    }

    # Transcript segments with speaker, timestamps, and translations
    segments = [
        {
            "speaker": "Speaker 1",
            "start": "00:00.000",
            "end": "00:05.230",
            "original": "Hello How are you ?",
            "bhashantar": "नमस्ते, आप कैसे हैं ?",
            "lipyantar": "Namaste, aap kaise hain ?",
        },
        {
            "speaker": "Speaker 2",
            "start": "00:05.230",
            "end": "00:10.146",
            "original": "I'm doing great, thanks.",
            "bhashantar": "मैं बढ़िया हूँ, धन्यवाद।",
            "lipyantar": "Main badhiya hoon, dhanyavaad.",
        },
        {
            "speaker": "Speaker 1",
            "start": "00:10.146",
            "end": "00:15.500",
            "original": "That's wonderful to hear!",
            "bhashantar": "यह सुनकर बहुत अच्छा लगा!",
            "lipyantar": "Yah sunkar bahut accha laga!",
        },
    ]

    # Prepare context for template
    context = {
        "soundfile": soundfile,
        "segments": segments,
    }

    return render(request, "sound.html", context)
