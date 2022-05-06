from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy

from .forms import RegistrationForm

User = get_user_model()


# User.objects.create(ghdkg)
class RegisterView(CreateView):
    model = User
    template_name = 'register.html'
    form_class = RegistrationForm
    success_url = 'https://mail.google.com/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['register_form'] = self.get_form(self.get_form_class())
        return context


class SignInView(LoginView):
    template_name = 'login.html'
    success_url = reverse_lazy('product_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_form'] = self.get_form(self.get_form_class())
        return context


def activate(request, activation_code):
    user = get_object_or_404(User, activation_code=activation_code)
    user.is_active = True
    user.activation_code = ''
    user.save()
    return redirect(reverse_lazy('login'))