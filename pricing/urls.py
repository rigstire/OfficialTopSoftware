from django.urls import path
from .views import pricing_view
from django.shortcuts import render

urlpatterns = [
    path("pricing/", pricing_view, name="pricing"),
]
