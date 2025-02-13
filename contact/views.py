from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm


def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            phone = form.cleaned_data["phone"]
            services = form.cleaned_data.get("services", "Not provided")  # Avoid KeyError if not included
            message = form.cleaned_data["message"]

            # Send an email to notify the owner
            send_mail(
                subject=f"New Contact Message from {name}",
                message=f"Name: {name}\nEmail: {email}\nPhone: {phone}\nService: {services}\n\nMessage:\n{message}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,
            )

            return redirect("contact_success")  # Redirect to success page after submission

    else:
        form = ContactForm()

    return render(request, "contact.html", {"form": form})
