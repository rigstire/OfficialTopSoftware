# sales_application/forms.py
from django import forms
from .models import SalesApplication

class SalesApplicationForm(forms.ModelForm):
    class Meta:
        model = SalesApplication
        fields = [
            'first_name', 'last_name', 'email', 'phone_number',
            'resume', 'has_bachelors_degree', 'degree_details',
            'has_worked_sales_before', 'years_of_sales_experience',
            'previous_work_experience', 'educational_experience',
            'is_certified_sales_professional', 'can_relocate',
            'has_own_vehicle', 'cover_letter'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your last name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your.email@example.com'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(123) 456-7890'}),
            'resume': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf'}),
            'has_bachelors_degree': forms.Select(attrs={'class': 'form-control'}),
            'degree_details': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Degree, university, and graduation year'
            }),
            'has_worked_sales_before': forms.Select(attrs={'class': 'form-control'}),
            'years_of_sales_experience': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': '0'
            }),
            'previous_work_experience': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Describe your previous work experience...'
            }),
            'educational_experience': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'List your educational background and qualifications...'
            }),
            'is_certified_sales_professional': forms.Select(attrs={'class': 'form-control'}),
            'can_relocate': forms.Select(attrs={'class': 'form-control'}),
            'has_own_vehicle': forms.Select(attrs={'class': 'form-control'}),
            'cover_letter': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Optional: Include a cover letter or additional information...'
            }),
        }
        help_texts = {
            'resume': 'Please upload your resume as a PDF file',
            'years_of_sales_experience': 'Enter 0 if you have no sales experience',
        }