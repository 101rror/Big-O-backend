from django.urls import path
from .views import analyze_code

urlpatterns = [
    path("analyze/", analyze_code, name="analyze_code"),
]
