"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path

from api import urls
from myapp import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(urls)),
    path("", views.show_employees, name="show_employees"),
    path("filter/", views.filter_example, name="show_employee_with_filters"),
    path("aggregate/", views.aggregate_example, name="show_aggregate_data"),
    path("update/", views.update_example, name="update_example"),
    path("chat/", views.chat, name="chat"),
    path("sound/", views.sound, name="sound"),
]
