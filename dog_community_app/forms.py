from django import forms

from .models import ContactUs, Newsletter, Reports

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

class MissingDogForm(forms.ModelForm):
    # model forms
    class Meta:
        model = Reports
        fields = [
            'dog',
            'breed',
            'reporter',
            'last_known_location',
            'category'
        ]
        widgets = {
            'message': forms.Textarea(attrs={'cols': 80, 'rows': 20})
        }

class NewsletterForm(forms.ModelForm):
    # model forms
    class Meta:
        model = Newsletter
        fields = '__all__'