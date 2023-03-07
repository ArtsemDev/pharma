from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.utils.translation import gettext as _


class UserRegisterForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                'class': 'input100',
                'name': 'password1',
                'placeholder': 'Enter Password'
            }
        ),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                'class': 'input100',
                'name': 'password1',
                'placeholder': 'Re-Enter Password'
            }
        ),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'input100',
                'name': 'password1',
                'placeholder': 'Enter Username'
            }
        )
    )


class LoginForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(
            attrs={
                'autofocus': True,
                'class': 'input100',
                'name': 'password1',
                'placeholder': 'Enter Username'
            }
        )
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                'class': 'input100',
                'name': 'password1',
                'placeholder': 'Re-Enter Password'
            }
        ),
    )
