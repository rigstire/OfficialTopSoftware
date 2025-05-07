from django import forms
from django_recaptcha.fields import ReCaptchaField

class ContactForm(forms.Form):
    captcha = ReCaptchaField()
    name = forms.CharField(
        max_length=255, 
        required=True, 
        widget=forms.TextInput(attrs={'placeholder': 'Your Name', 'class': 'cs-input'})
    )
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={'placeholder': 'Your Email', 'class': 'cs-input'})
    )
    phone = forms.CharField(
        max_length=20, 
        required=True, 
        widget=forms.TextInput(attrs={'placeholder': 'Your Phone', 'class': 'cs-input'})
    )

    message = forms.CharField(
        required=True, 
        widget=forms.Textarea(attrs={'placeholder': 'Write your message...', 'class': 'cs-input cs-textarea'})
    )
