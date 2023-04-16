from django.contrib.auth import views
from django.urls import path

from .views import CustomLoginView, SignUpView

urlpatterns = [
    path("login", CustomLoginView.as_view(), name="login"),
    path("logout", views.LogoutView.as_view(next_page="login"), name="logout"),
    path("signup", SignUpView.as_view(), name="signup"),
]
