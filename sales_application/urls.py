from django.urls import path
from .views import sales_application_view, application_success

urlpatterns = [
    path('', sales_application_view, name='sales_application'),
    path('success/', application_success, name='application_success'),
]

