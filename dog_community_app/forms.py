from django import forms

from .models import ContactUs, Newsletter, Reports, Dogs, User, Adoption

class ContactUsForm(forms.ModelForm):
    # model forms
    class Meta:
        model = ContactUs
        fields = '__all__'
        widgets = {
            'message': forms.Textarea(attrs={
                'cols': 40, 'rows': 5, 'placeholder': 'Message',
                'class': 'form-control my-2'
                }),
            'name': forms.TextInput(attrs={
                'placeholder': 'Your Name',
                'class': 'form-control my-2'
            }),
            'email': forms.TextInput(attrs={
                'placeholder': 'Email Address',
                'class': 'form-control my-2'
                })

        }

class UserDetailsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'user_name',
            'user_contact',
            'user_email'
        ]
        widgets = {
            'user_name': forms.TextInput(attrs={
                'placeholder': 'Your Name',
                'class': 'form-control my-2'
            }),
            'user_contact': forms.TextInput(attrs={
                'placeholder': 'Phone Number',
                'class': 'form-control my-2'
            }),
            'user_email': forms.TextInput(attrs={
                'placeholder': 'Email Address',
                'class': 'form-control my-2'
            }),
        }

class AdoptionDogDetailsForm(forms.ModelForm):
    class Meta:
        model = Dogs
        fields = [
            'dog_name'
        ]
        widgets = {
            'dog_name': forms.TextInput(attrs={
                'placeholder': "Dog's Name",
                'class': 'form-control my-2'
            }),
        }
class MissingDogDetails(forms.ModelForm):
    class Meta:
        model = Dogs
        fields = [
            'dog_name',
            'dog_age',
            'dog_color',
            'dog_image',
            'unique_identification',
            'is_disable',
            'disability'            
        ]
        widgets = {
            'dog_name': forms.TextInput(attrs={
                'placeholder': "Dog's Name",
                'class': 'form-control my-2'
            }),
            'dog_age': forms.TextInput(attrs={
                'placeholder': "Dog's Age",
                'class': 'form-control my-2'
            }),
            'dog_color': forms.TextInput(attrs={
                'placeholder': "Dog's color",
                'class': 'form-control my-2'
            }),
            'unique_identification': forms.Textarea(attrs={
                'cols': 50, 'rows': 3,
                'placeholder': "Dog's identification (unique)",
                'class': 'form-control my-2'
            }),
            'is_disable': forms.RadioSelect(),
            'disability': forms.TextInput(attrs={
                'placeholder': "Dog's identification (unique)",
                'class': 'form-control my-2'
            })
            
        }
        
class MissingDogReporter(forms.ModelForm):
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
            'description': forms.Textarea(attrs={'cols': 80, 'rows': 20})
        }

class NewsletterForm(forms.ModelForm):
    # model forms
    class Meta:
        model = Newsletter
        fields = '__all__'