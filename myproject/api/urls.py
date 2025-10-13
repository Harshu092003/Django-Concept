from django.urls import path

from . import views

urlpatterns = [
    path("", views.get_method, name="get"),
    path("post", views.post_method, name="post"),
    path("put/<str:pk>", views.put_method, name="put"),
    path("delete/<str:pk>", views.delete_method, name="delete"),
]
