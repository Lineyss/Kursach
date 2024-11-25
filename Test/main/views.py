from guardian.shortcuts import assign_perm, get_objects_for_user
from django.http import HttpResponse, FileResponse, JsonResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .models import Folder, File, FileFolder, Teg
from django.contrib.auth.models import Permission
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.conf import settings
from .forms import *
import zipfile

# Create your views here.

@login_required
def main(request, path='/'):
    IDFolder = None
    page_number = request.GET.get("page")

    if path != '/':
        path = '/' + path
        try:
            IDFolder = Folder.objects.get(Path=path)
            page_number = 1
        except:
            return render(request, 'main/main.html', {'error_message': 'Такой директории не существует', "path": path})

    files = File.objects.filter(Owner=request.user, IDFolder = IDFolder)
    folders = Folder.objects.filter(Owner=request.user, IDFolder = IDFolder)

    files_folders = list(files) + list(folders)
    
    teg = Teg.objects.filter(IDUser=request.user)

    paginator = Paginator(files_folders, 30)
    page_number = page_number
    page_obj = paginator.get_page(page_number)

    file_form = FileForm(initial={"Owner": request.user, 'IDFolder': IDFolder})
    folder_form = FolderForm(initial={"Owner": request.user, 'IDFolder': IDFolder})
    
    return render(request, 'main/main.html', {"page_obj": page_obj, 
                                              "file_form": file_form, 
                                              "folder_form": folder_form,
                                              "path": path,
                                              'error_message': '',
                                              "tegs": teg})

@login_required
def main_available(request, path='/'):
    IDFolder = None
    page_number = request.GET.get("page")

    if path != '/':
        path = '/' + path
        try:
            IDFolder = Folder.objects.get(Path=path)
            page_number = 1
        except:
            return render(request, 'main/main.html', {'error_message': 'Такой директории не существует', "path": path})
    
    files = File.objects.filter(Owner=request.user, IDFolder = IDFolder)
    folders = Folder.objects.filter(Owner=request.user, IDFolder = IDFolder)

    files_folders = list(files) + list(folders)
    
    teg = Teg.objects.filter(IDUser=request.user)

    paginator = Paginator(files_folders, 30)
    page_number = page_number
    page_obj = paginator.get_page(page_number)

    file_form = FileForm(initial={"Owner": request.user, 'IDFolder': IDFolder})
    folder_form = FolderForm(initial={"Owner": request.user, 'IDFolder': IDFolder})
    
    return render(request, 'main/main.html', {"page_obj": page_obj, 
                                              "file_form": file_form, 
                                              "folder_form": folder_form,
                                              "path": path,
                                              'error_message': '',
                                              "tegs": teg})

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
def tegs(request):
    form = None
    
    if request.POST:
        form = TegForm(request.POST)
        if form.is_valid:
            form.save()
        return redirect('tegs')
    else:
        form = TegForm(initial={"IDUser": request.user, 'Title': request.GET.get('Title')})

    tegs = Teg.objects.filter(IDUser=request.user)
    paginator = Paginator(list(tegs), 200)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'main/tegs.html', {'form': form, 'page_obj': page_obj})

@login_required
def update_teg(request, id):
    if request.POST:
        teg = None

        try:
            teg = Teg.objects.get(id=id)
        except:
            return HttpResponse('Не удалось обновить тег, попробуйте позже =(',status=400)

        form = TegForm(request.POST, instance=teg)
        if form.is_valid:
            instance  = form.save()
            return JsonResponse({
                'id': instance.id,
                'title': instance.Title,
                'color': instance.Color
            }, status=200)    
        
        return JsonResponse(form.errors, status=400)
    
    return HttpResponse(status=400)

@login_required
def delete_teg(request, id):
    if request.POST:

        try:
            teg = Teg.objects.get(id=id)
            teg.delete()
            return HttpResponse(status=200)
        except:
            return HttpResponse('Не удалось удалить тег, попробуйте позже =(',status=400)
    
    return HttpResponse(status=400)

@login_required
def add_teg_to_file_folder(request, teg_id, file_folder_id):
    if request.POST:
        try:
            teg_id = Teg.objects.get(id=teg_id)
        except:
            return HttpResponse('Не удалось найти папку',status=400)
        
        try:
            file_folder_id = FileFolder.objects.get(id=file_folder_id)
            file_folder_id.IDTeg = teg_id
            file_folder_id.save()
            return HttpResponse(status=200)
        except:
            return HttpResponse('Не удалось найти папку/файл', status=400)
        
    return HttpResponse(status=400)

@login_required
def create_access_url(request, id):
    if request.POST:
        access_token = get_random_secret_key()

    return HttpResponse(status=400)

@login_required
def open_access(request):
    pass

# Поделится 

# Доделать графики
## Добавить возоможность смотреть график по временным отрезкам
### Создать еще какой-то график
# Скачивание бекапа базы данных
# Открытие файла (если будет желание)

@login_required
def delete_file_folder(request, id):
    if request.method == 'POST':
        try:
            fileFolder = FileFolder.objects.get(id=id)
            if not request.user.has_perm('delete', fileFolder.get_file_or_folder()):
                return HttpResponseForbidden("У вас нет прав для удаления этого файла/папки.")
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
                if not request.user.has_perm('update', fileFolder.get_file_or_folder()):
                    return HttpResponseForbidden("У вас нет прав для измнения названия этого файла/папки.")
                
                file = fileFolder.get_file_or_folder()

                file.Title = title
                file.save()

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
                permissions = Permission.objects.filter(content_type__model='Folder')
                for perm in permissions:
                    assign_perm(perm.name, request.user, file_instance)
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
                permissions = Permission.objects.filter(content_type__model='Folder')
                for perm in permissions:
                    assign_perm(perm.name, request.user, folder_instance)
                return HttpResponse(f'{folder_instance.IDFileFolder.id}:{folder_instance.Title}', status=200)
            except Exception as e:
                return HttpResponse(e, status=400)
        print(form.errors)
        
    return HttpResponse('Не удалось создать папку, попробуйте позже', status=400)

@login_required
def move_file_folder(request, idMoveFileFolder, idToMoveFolder):
    if request.method == 'POST':
        fileFolder = None
        toFileFolder = None

        try:
            _fileFolder = FileFolder.objects.get(id = idMoveFileFolder)
            fileFolder = _fileFolder.get_related_file()
            if fileFolder is None:
                fileFolder = _fileFolder.get_related_folder()

            if not request.user.has_perm('open', fileFolder):
                return HttpResponseForbidden("У вас нет прав для перемещания этого файла/папки.")
        except:
            return HttpResponse('Не удалось найти файл/папку для перемещения', status=400)
        
        try:
            toFileFolder = FileFolder.objects.get(id = idToMoveFolder).folder
        except:
            return HttpResponse('Не удалось найти папку куда перемещать', status=400)
    
        if not request.user.has_perm('open', fileFolder):
            return HttpResponseForbidden("У вас нет прав для перемещания в эту папку.")
        
        fileFolder.IDFolder = toFileFolder
        fileFolder.save()

        return HttpResponse(status=200)

    return HttpResponse(status=400)

def addFilesToZip(zip, parent_folder):
    for file in parent_folder.files.all():
        zip.write(file.File.path, file.Title)
    
    for folder in parent_folder.folder_set.all():
        addFilesToZip(zip, folder)

@login_required
def download(request, id):
    if request.method == 'GET':
        path = None
        
        file_folder = FileFolder.objects.filter(id=id).first() 
        file = file_folder.get_related_file()

        if file is None:
            file = file_folder.get_related_folder()

            if not request.user.has_perm('download', file):
                return HttpResponseForbidden("У вас нет прав для скачивания этой папки.")
            
            file.Title += ".zip"
            zip_path = settings.ZIP_DIR / file.Title

            if os.path.exists(zip_path):
                os.remove(zip_path)

            with zipfile.ZipFile(zip_path, 'w') as zip:
                addFilesToZip(zip, file)

            path = zip_path
        else:
            if not request.user.has_perm('download', file):
                return HttpResponseForbidden("У вас нет прав для скачивания этого файла.")
            path = file.File.path

        file_download = open(path, "rb")
        response = FileResponse(file_download)
        response['Content-Disposition'] = f'attachment; filename="{file.Title}"'
                
        return response
    else:
        return HttpResponse('Не удалось найти файл =(', status=400)