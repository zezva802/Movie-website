from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelForm, NumberInput
from .models import Review, Profile
from django.contrib.auth.models import User


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'review_text']
        widgets = {
            'rating': NumberInput(attrs={'min': 1, 'max': 10}),
        }
        labels = {
            'rating': 'შეფასება',
            'review_text': 'კომენტარი'
        }


class UserRegisterForm(UserCreationForm):
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'profile_picture']


class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(ModelForm):
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ['profile_picture']
