from django import forms
from django.contrib.auth.forms import UserCreationForm
from Echo.accounts.models import UserProfile


class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = UserProfile
        fields = ('email', 'username', 'password1', 'password2')


class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture']
