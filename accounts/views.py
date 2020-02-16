from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views import generic
from .models import MyUser
from .forms import CustomUserCreationForm

class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'

# from django.contrib.auth.mixins import LoginRequiredMixin
# class MyView(LoginRequiredMixin, View): を入れるとログインの管理ができる
