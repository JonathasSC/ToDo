from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
# Create your views here.

@method_decorator(csrf_protect, name='dispatch')
class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'