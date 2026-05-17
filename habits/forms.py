from django import forms
from django.contrib.auth.models import User

from .models import UserProfile, PublicComment


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


class EditProfileForm(forms.Form):
    """
    Edit profile details and optionally change password + avatar.
    - full_name -> user.first_name
    - username  -> user.last_name (display handle)
    - avatar    -> UserProfile.avatar
    - new_password1/new_password2 -> user.set_password if provided
    """
    full_name = forms.CharField(max_length=150, required=True, label='Full Name')
    username = forms.CharField(max_length=150, required=False, label='Username')
    avatar = forms.ImageField(required=False, label='Profile Image')
    new_password1 = forms.CharField(
        label='New Password',
        required=False,
        widget=forms.PasswordInput,
    )
    new_password2 = forms.CharField(
        label='Confirm Password',
        required=False,
        widget=forms.PasswordInput,
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

        self.fields['full_name'].initial = self.user.first_name or ''
        self.fields['username'].initial = self.user.last_name or ''
        # file field doesn't need initial for our purposes
        self.fields['avatar'].widget.attrs['accept'] = 'image/*'

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('new_password1')
        p2 = cleaned.get('new_password2')

        if p1 or p2:
            # If one is filled, both must be and they must match
            if not p1 or not p2:
                raise forms.ValidationError("Please enter the new password twice.")
            if p1 != p2:
                raise forms.ValidationError("New password and confirmation do not match.")
            if len(p1) < 8:
                raise forms.ValidationError("Password must be at least 8 characters long.")

        return cleaned

    def save(self):
        full_name = (self.cleaned_data.get('full_name') or '').strip()
        username = (self.cleaned_data.get('username') or '').strip()
        new_password = self.cleaned_data.get('new_password1')
        avatar = self.cleaned_data.get('avatar')

        # Update user fields
        self.user.first_name = full_name
        self.user.last_name = username

        if new_password:
            self.user.set_password(new_password)

        self.user.save()

        # Update or create profile avatar
        profile, _ = UserProfile.objects.get_or_create(user=self.user)
        if avatar:
            profile.avatar = avatar
            profile.save()

        return self.user


class PublicCommentForm(forms.ModelForm):
    """
    Form for posting a public comment, limited to 2500 words.
    """
    class Meta:
        model = PublicComment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 3,
                'class': 'comments-textarea',
                'placeholder': 'Write a comment (max 2500 words)…',
            }),
        }

    def clean_text(self):
        text = self.cleaned_data.get('text', '') or ''
        # Count words by splitting on whitespace
        word_count = len(text.split())
        if word_count > 2500:
            raise forms.ValidationError(
                "Comments can't be longer than 2500 words."
            )
        return text