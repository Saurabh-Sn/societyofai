from django import forms
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
from django.contrib.auth.hashers import make_password
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm
from .models import User


class RegisterForm(forms.Form):
    """
    create user
    """
    email = forms.EmailField(max_length=254, required=True, )
    first_name = forms.CharField(max_length=254, required=True, )
    last_name = forms.CharField(max_length=254, required=True, )
    password = forms.CharField(min_length=8, widget=forms.PasswordInput(), required=True)
    password2 = forms.CharField(min_length=8, widget=forms.PasswordInput(), required=True, label='Confirm Password')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        existing_user = User.objects.filter(email=email)
        if existing_user.count() > 0:
            raise forms.ValidationError(_("User already exists with this email. Please try with different email."))
        return email

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if not password2:
            raise forms.ValidationError(_("You must confirm your password."))
        if password != password2:
            raise forms.ValidationError(_("Your passwords do not match."))
        return password2

    def save(self):
        data = self.cleaned_data
        user = User(
            email=data['email'],
            is_active=True,
            password=make_password(data['password']),
            first_name=data['first_name'],
            last_name=data['last_name']

        )
        return user.save()


class FrontendAuthenticationForm(AuthenticationForm):
    """
    """

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                _("Account has been deactivated. Contact admin."),
                code='inactive',
            )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username is not None and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            user = User.objects.filter(email=username).first()
            if user:
                if user.check_password(password) and not user.is_active:
                    raise forms.ValidationError(
                        _("Account has been deactivated. Contact admin."),
                        code='inactive',
                    )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data
