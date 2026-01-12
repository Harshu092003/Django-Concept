from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views
from .views import (LoginView, PasswordResetConfirmView,
                    PasswordResetRequestView, RegisterView)

urlpatterns = [
    path("", views.get_method, name="get"),
    path("post", views.post_method, name="post"),
    path("put/<str:pk>", views.put_method, name="put"),
    path("delete/<str:pk>", views.delete_method, name="delete"),
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
    path("password-reset/", PasswordResetRequestView.as_view()),
    path("password-reset-confirm/", PasswordResetConfirmView.as_view()),
]
