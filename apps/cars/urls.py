from django.urls import path

from . import views

app_name = "cars"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
]