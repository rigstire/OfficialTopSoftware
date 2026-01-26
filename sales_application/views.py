from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
import logging
from .forms import SalesApplicationForm

logger = logging.getLogger(__name__)

def sales_application_view(request):
    """View to handle sales application form submission"""
    if request.method == 'POST':
        form = SalesApplicationForm(request.POST, request.FILES)
        
        # Log form data for debugging
        logger.info(f"Form submission received - POST data: {request.POST}")
        logger.info(f"Files received: {list(request.FILES.keys()) if request.FILES else 'None'}")
        
        if form.is_valid():
            try:
                # Log before saving
                logger.info("Form is valid, attempting to save...")
                if 'resume' in request.FILES:
                    resume_file = request.FILES['resume']
                    logger.info(f"Resume file: {resume_file.name}, size: {resume_file.size} bytes, content_type: {resume_file.content_type}")
                
                # Check if B2 storage is configured
                use_b2 = getattr(settings, 'USE_B2_STORAGE', False)
                logger.info(f"B2 Storage enabled: {use_b2}")
                if use_b2:
                    logger.info(f"B2 Bucket: {getattr(settings, 'AWS_STORAGE_BUCKET_NAME', 'NOT SET')}")
                    logger.info(f"B2 Endpoint: {getattr(settings, 'AWS_S3_ENDPOINT_URL', 'NOT SET')}")
                
                # Save the application
                application = form.save()
                logger.info(f"Application saved successfully! ID: {application.id}, Email: {application.email}")
                
                # Log the resume file path
                if application.resume:
                    logger.info(f"Resume saved to: {application.resume.name}")
                    logger.info(f"Resume URL: {application.resume.url if hasattr(application.resume, 'url') else 'N/A'}")
                
                messages.success(request, 'Your application has been submitted successfully!')
                return redirect('application_success')
                
            except Exception as e:
                # Log the full error
                logger.error(f"Error saving application: {type(e).__name__}: {str(e)}", exc_info=True)
                messages.error(request, f'An error occurred while saving your application. Please try again. Error: {str(e)}')
        else:
            # Log form errors
            logger.warning(f"Form validation failed. Errors: {form.errors}")
            logger.warning(f"Form non-field errors: {form.non_field_errors()}")
            for field, errors in form.errors.items():
                logger.warning(f"Field '{field}' errors: {errors}")
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SalesApplicationForm()
    
    return render(request, 'sales_application/application.html', {'form': form})

def application_success(request):
    """View to display success message after application submission"""
    return render(request, 'sales_application/success.html')
