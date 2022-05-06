from django.forms import ModelForm, CharField, PasswordInput, ValidationError
from django.contrib.auth import get_user_model

from .helpers import send_activation_mail

User = get_user_model()


class RegistrationForm(ModelForm):
    password = CharField(min_length=6,
                         max_length=20,
                         required=True,
                         widget=PasswordInput)

    password_confirmation = CharField(min_length=6,
                                      max_length=20,
                                      required=True,
                                      widget=PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'password', 'password_confirmation')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('User with given email already exists')
        return email

    def clean(self):
        data = self.cleaned_data
        password1 = data.get("password")
        password2 = data.pop('password_confirmation')
        if password1 != password2:
            raise ValidationError('Passwords do not match')
        return data

    def save(self):
        user = User.objects.create_user(**self.cleaned_data)
        send_activation_mail(user)
        return user