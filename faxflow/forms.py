from django import forms


class FaxFlowPilotForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Your name',
            'class': 'cs-input',
            'autocomplete': 'name',
        }),
    )
    practice_name = forms.CharField(
        max_length=255,
        required=True,
        label='Practice name',
        widget=forms.TextInput(attrs={
            'placeholder': 'Practice or clinic name',
            'class': 'cs-input',
            'autocomplete': 'organization',
        }),
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Work email',
            'class': 'cs-input',
            'autocomplete': 'email',
        }),
    )
    phone = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Phone number',
            'class': 'cs-input',
            'autocomplete': 'tel',
        }),
    )
    workflow = forms.CharField(
        required=True,
        label='Tell us about your fax workflow',
        widget=forms.Textarea(attrs={
            'placeholder': 'How many faxes do you get? Who handles them today?',
            'class': 'cs-input cs-textarea',
            'rows': 5,
        }),
    )
