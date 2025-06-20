from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import User


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1',
                  'password2', 'username', 'university', 'department']


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']
