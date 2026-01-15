from django.db import models
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
import os

def validate_pdf_file(value):
    """Custom validator to ensure file is PDF"""
    ext = os.path.splitext(value.name)[1]
    if ext.lower() != '.pdf':
        raise ValidationError('Only PDF files are allowed.')

def validate_file_size(value):
    """Custom validator to ensure file size is less than 5MB"""
    max_size = 5242880  # 5MB in bytes
    if value.size > max_size:
        raise ValidationError(f'File size cannot exceed 5MB. Current file size: {value.size / 1024 / 1024:.2f}MB')

class SalesApplication(models.Model):
    # Personal Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    
    # Resume Upload
    resume = models.FileField(
        upload_to='resumes/%Y/%m/%d/',
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf']),
            validate_pdf_file,
            validate_file_size
        ],
        help_text='Upload your resume in PDF format (max 5MB)'
    )

    HAS_BACHELORS_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
        ('in_progress', 'In Progress'),
    ]
    
    has_bachelors_degree = models.CharField(
        max_length=12,
        choices=HAS_BACHELORS_CHOICES,
        verbose_name='Do you have a bachelor\'s degree?',
        default='no',
        help_text='Select "In Progress" if currently enrolled'
    )
    degree_details = models.TextField(
        blank=True,
        verbose_name='Degree Details (Optional)',
        help_text='If yes, please specify your degree, university, and graduation year'
    )    
    # Yes/No Questions
    HAS_WORKED_SALES_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    
    has_worked_sales_before = models.CharField(
        max_length=3,
        choices=HAS_WORKED_SALES_CHOICES,
        verbose_name='Have you worked in sales before?'
    )
    
    years_of_sales_experience = models.PositiveIntegerField(
        default=0,
        verbose_name='If yes, how many years of sales experience?'
    )
    
    # Work Experience (structured)
    previous_work_experience = models.TextField(
        help_text='Please describe your previous work experience in detail',
        blank=True
    )
    
    # Education (structured)
    educational_experience = models.TextField(
        help_text='Please list your educational background and qualifications',
        blank=True
    )
    
    # Additional Yes/No Questions
    IS_CERTIFIED_SALES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    is_certified_sales_professional = models.CharField(
        max_length=3,
        choices=IS_CERTIFIED_SALES,
        default='no',
        verbose_name='Are you a certified sales professional?'
    )
    
    CAN_RELOCATE = [
        ('yes', 'Yes'),
        ('no', 'No'),
        ('maybe', 'Maybe, depending on opportunity')
    ]
    can_relocate = models.CharField(
        max_length=5,
        choices=CAN_RELOCATE,
        verbose_name='Are you willing to relocate?'
    )
    
    HAS_VEHICLE = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    has_own_vehicle = models.CharField(
        max_length=3,
        choices=HAS_VEHICLE,
        verbose_name='Do you have reliable transportation?'
    )
    
    # Additional Information
    cover_letter = models.TextField(
        blank=True,
        help_text='Optional: Include a cover letter or additional information'
    )
    
    # Timestamps
    application_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    
    # Application Status
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('reviewed', 'Reviewed'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
        ('hired', 'Hired'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    
    # Metadata
    class Meta:
        verbose_name = 'Sales Application'
        verbose_name_plural = 'Sales Applications'
        ordering = ['-application_date']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def total_experience(self):
        """Calculate total sales experience"""
        if self.has_worked_sales_before == 'yes':
            return self.years_of_sales_experience
        return 0
    
    def clean(self):
        """Custom validation"""
        if self.has_worked_sales_before == 'no' and self.years_of_sales_experience > 0:
            raise ValidationError({
                'years_of_sales_experience': 'Cannot have sales experience if never worked in sales before.'
            })
