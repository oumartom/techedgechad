# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User

# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
# from .models import TrainingRegistration 

# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
# from .models import UserProfile

# class CustomUserCreationForm(UserCreationForm):
#     first_name = forms.CharField(
#         max_length=30, 
#         required=True,
#         widget=forms.TextInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Votre prénom'
#         })
#     )
#     last_name = forms.CharField(
#         max_length=30, 
#         required=True,
#         widget=forms.TextInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Votre nom'
#         })
#     )
#     phone = forms.CharField(
#         max_length=20, 
#         required=True,
#         widget=forms.TextInput(attrs={
#             'class': 'form-control',
#             'placeholder': '+235 XX XX XX XX'
#         }),
#         help_text="Format: +235 suivi de 8 chiffres"
#     )
    
#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'email', 'phone', 'username', 'password1', 'password2']
#         widgets = {
#             'email': forms.EmailInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'exemple@email.com'
#             }),
#             'username': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Choisissez un nom d\'utilisateur'
#             }),
#         }
    
#     def clean_phone(self):
#         phone = self.cleaned_data.get('phone')
        
#         # Nettoyer le numéro
#         phone = phone.replace(' ', '').replace('-', '')
        
#         # Vérifier le format +235
#         if not phone.startswith('+235'):
#             raise forms.ValidationError("Le numéro doit commencer par +235 (Tchad)")
        
#         # Vérifier la longueur
#         if len(phone) != 12:  # +235 + 8 chiffres
#             raise forms.ValidationError("Le numéro doit avoir 8 chiffres après +235")
        
#         # Vérifier que ce sont des chiffres après +235
#         if not phone[4:].isdigit():
#             raise forms.ValidationError("Seuls les chiffres sont autorisés après +235")
        
#         return phone
    
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.first_name = self.cleaned_data['first_name']
#         user.last_name = self.cleaned_data['last_name']
#         user.email = self.cleaned_data['email']
        
#         if commit:
#             user.save()
            
#             # CRÉATION EXPLICITE du profil avec le téléphone
#             profile, created = UserProfile.objects.get_or_create(user=user)
#             profile.phone = self.cleaned_data['phone']
#             profile.save()  # ← N'OUBLIEZ PAS DE SAUVEGARDER !
        
#         return user
# class TrainingRegistrationForm(forms.ModelForm):
#     class Meta:
#         model = TrainingRegistration
#         fields = ['notes']
#         widgets = {
#             'notes': forms.Textarea(attrs={
#                 'class': 'form-control',
#                 'rows': 3,
#                 'placeholder': 'Pourquoi souhaitez-vous suivre cette formation ?',
#                 'maxlength': '500'
#             }),
#         }
#         labels = {
#             'notes': 'Message (optionnel)'
#         }
# # class CustomUserCreationForm(UserCreationForm):
# #     email = forms.EmailField(
# #         required=True,
# #         widget=forms.EmailInput(attrs={
# #             'class': 'form-control',
# #             'placeholder': 'Votre adresse email'
# #         })
# #     )
    
# #     class Meta:
# #         model = User
# #         fields = ['username', 'email', 'password1', 'password2']
# #         widgets = {
# #             'username': forms.TextInput(attrs={
# #                 'class': 'form-control',
# #                 'placeholder': 'Nom d\'utilisateur'
# #             }),
# #         }
    
# #     def __init__(self, *args, **kwargs):
# #         super().__init__(*args, **kwargs)
# #         # Ajouter des classes Bootstrap aux champs de mot de passe
# #         self.fields['password1'].widget.attrs.update({'class': 'form-control'})
# #         self.fields['password2'].widget.attrs.update({'class': 'form-control'})
# class ContactForm(forms.Form):
#     name = forms.CharField(label='Votre Nom', max_length=100)
#     email = forms.EmailField(label='Votre Email')
#     subject = forms.CharField(label='Objet', max_length=200)
#     message = forms.CharField(label='Message', widget=forms.Textarea)
# class CustomUserCreationForm(UserCreationForm):
#     first_name = forms.CharField(...)
#     last_name = forms.CharField(...)
#     phone = forms.CharField(...)
#     email = forms.EmailField(...)

#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'email', 'phone', 'username', 'password1', 'password2']
# from .models import Subscriber, TrainingRegistration

# class SubscriberForm(forms.ModelForm):
#     class Meta:
#         model = Subscriber
#         fields = ['email']

# from .models import BlogComment

# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = BlogComment
#         fields = ['content']
#         widgets = {
#             'content': forms.Textarea(attrs={
#                 'class': 'form-control',
#                 'rows': 4,
#                 'placeholder': 'Votre commentaire...',
#                 'maxlength': '1000'
#             }),
#         }
#         labels = {
#             'content': ''
#         }
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, TrainingRegistration, Subscriber, BlogComment


class CustomUserCreationForm(UserCreationForm):
    phone = forms.CharField(max_length=20, required=False, label="Téléphone")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2', 'phone']

    def save(self, commit=True):
        user = super().save(commit=commit)  # Création de l'utilisateur
        phone = self.cleaned_data.get('phone')

        if commit:
            # On met à jour le profil lié
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.phone = phone
            profile.save()

        return user


class TrainingRegistrationForm(forms.ModelForm):
    class Meta:
        model = TrainingRegistration
        fields = ['notes']
        widgets = {
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Pourquoi souhaitez-vous suivre cette formation ?',
                'maxlength': '500'
            }),
        }
        labels = {
            'notes': 'Message (optionnel)'
        }


class ContactForm(forms.Form):
    name = forms.CharField(label='Votre Nom', max_length=100)
    email = forms.EmailField(label='Votre Email')
    subject = forms.CharField(label='Objet', max_length=200)
    message = forms.CharField(label='Message', widget=forms.Textarea)


class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']


class CommentForm(forms.ModelForm):
    class Meta:
        model = BlogComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Votre commentaire...',
                'maxlength': '1000'
            }),
        }
        labels = {
            'content': ''
        }
