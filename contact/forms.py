from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=255, required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=True)
    services = forms.ChoiceField(
        choices=[
            ("New Construction", "New Construction"),
            ("Remodels", "Remodels"),
            ("Cabinets", "Cabinets"),
        ],
        required=True,
    )
    message = forms.CharField(widget=forms.Textarea, required=True)
