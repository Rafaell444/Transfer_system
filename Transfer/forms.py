from django import forms
from .models import File
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['title', 'file', 'transfer_to']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(FileForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(FileForm, self).save(commit=False)
        if self.request is not None:
            # set the host field to the email of the authenticated user
            instance.host = self.request.user.email
        if commit:
            instance.save()
        return instance


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')

    class Meta:
        model = CustomUser
        fields = ('email', 'name', 'password1', 'password2')


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=254, required=True, widget=forms.EmailInput(attrs={'autofocus': True}))
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )

    error_messages = {
        'invalid_login': "Please enter a correct email address and password. Note that both fields may be case-sensitive.",
        'inactive': "This account is inactive.",
    }
