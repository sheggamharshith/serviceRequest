from django.urls import path

from .views import (CreateServiceView, DeleteServiceView, DetailServiceView,
                    HomePageView, LandingPageView, ServiceView)

urlpatterns = [
    path("home", HomePageView.as_view(), name="home"),
    path("", LandingPageView.as_view(), name="landing"),
    path("service-request", ServiceView.as_view(), name="service_request_list"),
    path(
        "service-request/<int:pk>",
        DetailServiceView.as_view(),
        name="service_request_detail",
    ),
    path(
        "service-request/add",
        CreateServiceView.as_view(),
        name="service_request_create",
    ),
    path(
        "service-request/<int:pk>/delete",
        DeleteServiceView.as_view(),
        name="service_request_delete",
    ),
]
