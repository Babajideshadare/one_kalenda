from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.Form):
    full_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput,
        required=True,
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput,
        required=True,
    )

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        # We use email as username internally
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned

    def save(self):
        full_name = self.cleaned_data['full_name']
        email = self.cleaned_data['email'].lower()
        password = self.cleaned_data['password1']

        user = User.create_user(
            username=email,   # use email as username
            email=email,
            password=password,
        )
        user.first_name = full_name  # store full name in first_name field
        user.save()
        return user


class ProfileForm(forms.Form):
    """
    Edit profile:
    - Name      -> user.first_name
    - Username  -> user.last_name (display handle only)
    - Email     -> user.email AND user.username (login identifier)
    """
    name = forms.CharField(max_length=150, required=False, label='Name')
    username = forms.CharField(max_length=150, required=False, label='Username')
    email = forms.EmailField(required=True, label='Email')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

        self.fields['name'].initial = self.user.first_name or ''
        self.fields['username'].initial = self.user.last_name or ''
        self.fields['email'].initial = self.user.email or ''

        # Match UI placeholder
        self.fields['username'].widget.attrs['placeholder'] = 'No Username'

    def clean_email(self):
        email = (self.cleaned_data.get('email') or '').lower()
        if not email:
            raise forms.ValidationError("Email is required.")

        # Email is also used as username for login, so must be unique
        if User.objects.filter(username=email).exclude(pk=self.user.pk).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def save(self):
        name = (self.cleaned_data.get('name') or '').strip()
        username = (self.cleaned_data.get('username') or '').strip()
        email = self.cleaned_data['email'].lower()

        self.user.first_name = name
        self.user.last_name = username
        self.user.email = email
        self.user.username = email  # keep login identifier in sync
        self.user.save()
        return self.user