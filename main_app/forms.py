from django.contrib.auth.forms import UserChangeForm
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
