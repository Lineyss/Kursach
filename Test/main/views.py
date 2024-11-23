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
        fields = ['IDFolder', 'File', 'Owner']

class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ['IDFolder', 'Title', 'Owner']

@login_required
def main(request, path='/'):
    IDFolder = None

    if path != '/':
        path = '/' + path
        try:
            IDFolder = Folder.objects.get(Path=path)
        except:
            return render(request, 'main/main.html', {'error_message': 'Такой директории не существует', "path": path})

    files = File.objects.filter(Owner=request.user, IDFolder = IDFolder)
    folders = Folder.objects.filter(Owner=request.user, IDFolder = IDFolder)

    files_folders = list(files) + list(folders)

    paginator = Paginator(files_folders, 25)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    file_form = FileForm(initial={"Owner": request.user, 'IDFolder': IDFolder})
    folder_form = FolderForm(initial={"Owner": request.user, 'IDFolder': IDFolder})
    
    return render(request, 'main/main.html', {"page_obj": page_obj, 
                                              "file_form": file_form, 
                                              "folder_form": folder_form, 
                                              "path": path,
                                              'error_message': ''})

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

# Перетаскивать файл между папками
# Добавлнеие тега на файл/папку
# Поделится 
# Доделать графики
## Добавить возоможность смотреть график по временным отрезкам
### Создать еще какой-то график
# Скачивание бекапа базы данных
# Открытие файла (если будет желание)
# Скачивание папко / не давать возможность скачивай файлы

@login_required
def delete_file_folder(request, id):
    if request.method == 'POST':
        try:
            fileFolder = FileFolder.objects.get(id=id)
            fileFolder.delete()
            return HttpResponse(status=200)
        except:
            return HttpResponse('Не удалось удалить, попробуйте позже =(', status=400)
    return HttpResponse(status=400)

@login_required
def update_file_folder_name(request, id, title):
    if request.method == 'POST':
        if title:
            try:
                fileFolder = FileFolder.objects.get(id=id)
                file = fileFolder.get_related_file()
                folder = fileFolder.get_related_folder()

                if file:
                    file.Title  = title
                    file.save()
                elif folder:
                    folder.Title = title
                    folder.save()

                return HttpResponse(f'{fileFolder.id}:{title}', status=200)

            except:
                return HttpResponse('Не удалось изменить название, попробуйте позже =(', status=400)
        
    return HttpResponse(status=400)

@login_required
def file_create(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                file_instance = form.save()
                return HttpResponse(f'{file_instance.IDFileFolder.id}:{file_instance.Title}', status=200)
            except Exception as e:
                return HttpResponse(e, status=400)
        print(form.errors)
    return HttpResponse('Не удалось загрузить файл, попробуйте позже', status=400)

@login_required
def folder_create(request):     
    if request.method == 'POST':
        form = FolderForm(request.POST)
        if form.is_valid():
            try:
                folder_instance = form.save()
                return HttpResponse(f'{folder_instance.IDFileFolder.id}:{folder_instance.Title}', status=200)
            except Exception as e:
                return HttpResponse(e, status=400)
        print(form.errors)
        
    return HttpResponse('Не удалось создать папку, попробуйте позже', status=400)

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