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

        user = User.objects.create_user(
            username=email,   # use email as username
            email=email,
            password=password,
        )
        user.first_name = full_name  # store full name in first_name field
        user.save()
        return user