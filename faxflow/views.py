from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .forms import FaxFlowPilotForm


def faxflow_view(request):
    if request.method == 'POST':
        form = FaxFlowPilotForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            practice_name = form.cleaned_data['practice_name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            workflow = form.cleaned_data['workflow']

            send_mail(
                subject=f'FaxFlow Pilot Request from {name} ({practice_name})',
                message=(
                    f'Name: {name}\n'
                    f'Practice: {practice_name}\n'
                    f'Email: {email}\n'
                    f'Phone: {phone}\n\n'
                    f'Fax workflow:\n{workflow}'
                ),
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,
            )

            messages.success(
                request,
                'Thanks — we received your pilot request and will follow up soon.',
            )
            return redirect('faxflow')
    else:
        form = FaxFlowPilotForm()

    return render(request, 'faxflow.html', {'form': form})
