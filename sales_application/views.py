from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SalesApplicationForm

def sales_application_view(request):
    """View to handle sales application form submission"""
    if request.method == 'POST':
        form = SalesApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save()
            messages.success(request, 'Your application has been submitted successfully!')
            return redirect('application_success')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SalesApplicationForm()
    
    return render(request, 'sales_application/application.html', {'form': form})

def application_success(request):
    """View to display success message after application submission"""
    return render(request, 'sales_application/success.html')
