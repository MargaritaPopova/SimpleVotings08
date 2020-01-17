from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, ReadOnlyPasswordHashField
from django.contrib.auth.models import User


class EditProfileForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
        )
