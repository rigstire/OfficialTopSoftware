from django.urls import path
from .views import portfolio_view

urlpatterns = [
    path("portfolio", portfolio_view, name="portfolio"),
]
