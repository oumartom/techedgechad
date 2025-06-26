from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(label='Votre Nom', max_length=100)
    email = forms.EmailField(label='Votre Email')
    subject = forms.CharField(label='Objet', max_length=200)
    message = forms.CharField(label='Message', widget=forms.Textarea)
    
from .models import Subscriber

class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']
