from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm 
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.shortcuts import render

# Create your views here.

class SingUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/reg.html"

@login_required
def main(request):
    return render(request, 'main/main.html')