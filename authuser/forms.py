from wagtail.users.forms import UserEditForm, UserCreationForm
from django.utils.translation import gettext_lazy as _
from authuser.models import User

class CustomUserEditForm(UserEditForm):
    class Meta:
        model = User
        fields = '__all__'


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = '__all__'