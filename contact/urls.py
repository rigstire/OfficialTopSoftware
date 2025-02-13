from django.urls import path
from .views import contact_view

urlpatterns = [
    path("contact/", contact_view, name="contact"),
    path("contact/success/", lambda request: render(request, "contact_success.html"), name="contact_success"),
]
