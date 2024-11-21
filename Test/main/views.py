from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm 
from django.core.exceptions import ValidationError
from django.views.generic.edit import CreateView
from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
from .models import Folder, File, FileFolder
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.http import HttpResponse
from django import forms
import os

# Create your views here.

class SingUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/reg.html"

class UsernameChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']
    
    def clean_username(self):
        new_username = self.cleaned_data['username']
        if User.objects.filter(username=new_username).exists():
            raise ValidationError("Such a name already exists")

        return new_username

class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['File']

@login_required
def main(request):
    files = File.objects.filter(IDUser=request.user)
    folders = Folder.objects.filter(IDUser=request.user)

    files_folders = list(files) + list(folders)

    paginator = Paginator(files_folders, 25)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'main/main.html', {"page_obj": page_obj, "form": FileForm()})

@login_required
def profile(request):
    return render(request, 'main/profile_main.html')

@login_required
def change_username(request):
    if request.method == 'POST':
        form = UsernameChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(profile)
    else:
        form = UsernameChangeForm(instance=request.user)

    return render(request, 'main/profile_form.html', {'form': form})

@login_required
def delete_file_folder(request, id):
    if request.method == 'POST':
        FileFolder.objects.filter(id=id).first().delete()
    
    return redirect('main')

@login_required
def file_create(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                file_instance = form.save()
                file_instance.IDUser.add(request.user)
                return HttpResponse(f'{file_instance.IDFileFolder.id}: {file_instance.Title}', status=200)
            except Exception as e:
                return HttpResponse(e, status=400)
        print(form.errors)
    return HttpResponse('Не удалось загрузить файл, попробуйте позже', status=400)


# Нужно доделать. Файлы скачиваются но не правильного формата и названия
@login_required
def download(request, id):
    if request.method == 'GET':
        file_folder = FileFolder.objects.filter(id=id).first() 
        file = file_folder.get_related_file()
        file_download = open(file.File.path, "rb")
        response = FileResponse(file_download)
        response['Content-Disposition'] = f'attachment; filename="{file.Title}"'
        
        return response

    return HttpResponse('Не найти файл', status=400)