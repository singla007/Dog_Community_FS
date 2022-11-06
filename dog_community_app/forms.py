from django import forms

from .models import ContactUs, Newsletter

class ContactUsForm(forms.ModelForm):
    # model forms
    class Meta:
        model = ContactUs
        fields = [
            'name',
            'email',
            'message'
        ]
        widgets = {
            'message': forms.Textarea(attrs={'cols': 80, 'rows': 20})
        }

class NewsletterForm(forms.ModelForm):
    # model forms
    class Meta:
        model = Newsletter
        fields = '__all__'