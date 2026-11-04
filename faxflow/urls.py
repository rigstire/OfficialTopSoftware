from django.urls import path
from .views import faxflow_view

urlpatterns = [
    path('', faxflow_view, name='faxflow'),
]
